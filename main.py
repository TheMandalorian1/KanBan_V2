# ========================= Imports ==================================
from flask import Flask
from flask_restful import Api
from os import path
from flask_cors import CORS
from applications.models import ADD
from applications import workers

appli = None
api = None
celery = None
 
#Creating application
def initiate_app():
    #Creating a Flask instance
    appli = Flask(__name__, template_folder="templates") 
    appli.config['SECRET_KEY'] = "21f1001069"

    #Adding datatbase
    appli.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///addDB.sqlite3'
    appli.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #Initalizing database
    ADD.init_app(appli)
    appli.app_context().push() 
    #Initalizing API
    api = Api(appli)
    appli.app_context().push()

    CORS(appli)

    celery = workers.celery

    celery.conf.update(
        broker_url='redis://localhost:6379',
        result_backend='redis://localhost:6379'
    )
    celery.Task = workers.ContextTask
    appli.app_context().push()
    #Calling fun to create database
    initiate_DB(appli)
    return appli, api, celery

#Creating database
def initiate_DB(app):
    if path.exists('/addDB.sqlite3') == False:
        ADD.create_all()
    return True


# --------------------------------------------------
# Calling fun to create application
apple, api, celery = initiate_app()

# Import all the controllers so they are loaded
from applications.tasks import *

# from app import initiate_app
from applications.api import UserAPI, UserOUT, ListAPI, CardAPI, DashAPI, SummaryAPI, DetailsAPI, ExportAPI

api.add_resource(UserAPI, "/api/register", "/api/login")
api.add_resource(UserOUT, "/api/logout")
api.add_resource(ListAPI, "/api/createlist", "/api/elist/<int:listId>", "/api/dlist/<int:listId>", "/api/list/<int:listId>")
api.add_resource(CardAPI, "/api/<int:listId>/createcard", "/api/dcard/<int:cardId>", "/api/ecard/<int:cardId>", "/api/card/<int:cardId>")
api.add_resource(DashAPI, "/api/dashboard")
api.add_resource(SummaryAPI, "/api/summary")
api.add_resource(ExportAPI, "/api/export")
api.add_resource(DetailsAPI, "/api/details")

# Running the application
if __name__ == '__main__':
    apple.run(debug=True)

# users = User.query.all()
# print(users)