# ==================================================== Imports ===================================================
import time
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import create_access_token
from matplotlib import pyplot as plt
from flask import request, session, jsonify, send_from_directory
import applications.tasks
from flask_caching import Cache
from flask_restful import fields, marshal_with, reqparse, Resource, abort
from werkzeug.security import generate_password_hash, check_password_hash
import csv 
# from applications import models
from applications.models import User, List, Card, ADD
from datetime import datetime, timedelta, date
import re
from flask import current_app as capp
import matplotlib
matplotlib.use('Agg')


capp.config["JWT_SECRET_KEY"] = "21f1001069"  # Change this!
capp.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
capp.config["CACHE_TYPE"] = "redis"
capp.config['CACHE_REDIS_HOST'] = "localhost"
capp.config['CACHE_REDIS_PORT'] = 6379
capp.config['CACHE_REDIS_DB'] = 0
capp.config["CACHE_REDIS_URL"] = "redis://localhost:6379"  
capp.config['CACHE_DEFAULT_TIMEOUT'] = 500
jwt = JWTManager(capp)
cash = Cache(capp)

# ============================================ Custom ========================================================

td = datetime.now().strftime("%Y-%m-%d %H:%M")
# drange = {}
# for i in range(4,-1,-1):
#     drange[str(date.today()-timedelta(days = i))] = 0
statusList = ["Pending", "Completed", "Failed to complete"]
mailptr = r'\b[A-Za-z0-9._]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
nameptr = r'\b[A-Za-z0-9_ -]{2,}\b'
passptr = r'\b[A-Za-z0-9]{6,12}\b'

# ============================================ Error Code Dict =======================================================
errord = {
    "CE1": 'User Name should be string having length less than 31.',
    "CE2": 'A valid Email is required and should be string having length less than 101.',
    "CE3": 'Password should be string having length between 5 to 13.',
    "CE4": 'Email already exist. Please try with a different Email.',
    "CE5": 'Incorrect Password.',
    "CE6": 'User login is required, please login to continue.',

    "LE1": 'List name should be String having length less than 20.',
    "LE2": 'List description should be String having length less than 100.',
    "LE3": 'The list you want to edit does not exist.',
    "LE4": 'The list you want to delete does not exist.',

    "DE1": 'Card name should be String having length less than 20.',
    "DE2": 'Card description should be String having length less than 200.',
    "DE3": 'Card Deadline is required.',
    "DE4": 'Card status [Pending, Completed, Failed to complete] is required.',
    "DE5": 'The list in which you want to move the card is not found.',
    "DE6": 'Card not found.',
    "DE7": 'List not found.'
}



# ============================================ User API ==========================================================
User_register_out = {
    "User_id": fields.Integer,
    "User_name": fields.String,
    "User_email": fields.String,
    "User_pass": fields.String,
}

register_user_parser = reqparse.RequestParser()
register_user_parser.add_argument("name")
register_user_parser.add_argument("email")
register_user_parser.add_argument("password")


class UserAPI(Resource):
    @cash.cached(timeout=5)
    def get(self):
        arg = request.args
        email = arg.get("email")
        password = arg.get("password")

        check = User.query.filter_by(User_email=email).first()
        if check is not None:
            if check_password_hash(check.User_pass, password):
                session["cust"] = check.User_name
                session["cid"] = check.User_id
                access_token = create_access_token(identity=email)
                return jsonify(token=access_token)
            abort(400, message='Incorrect Password.')
        abort(404, message="User not found.")


    
    def post(self):
        args = register_user_parser.parse_args()
        name = args.get("name")
        email = args.get("email")
        password = args.get("password")

        check = User.query.filter_by(User_email=email).first()
        if check is None:
            print("hii")
            new_cust = User(
                User_name=name, User_email=email, User_pass=generate_password_hash(password, method='sha256'))
            ADD.session.add(new_cust)
            ADD.session.commit()
            check2 = User.query.filter_by(User_email=email).first()
            session["cust"] = check2.User_name
            session["cid"] = check2.User_id
            access_token = create_access_token(identity=email)
            return jsonify(token=access_token)

        abort(400, message='Email already exist. Please try with a different Email.')
    


class UserOUT(Resource):
    def get(self):
        session.clear()
        cash.clear()
        return 200


# ============================================ List API ================================================================
list_out = {
    "List_id": fields.Integer,
    "List_name": fields.String,
    # "List_desc": fields.String,
}

create_list_parser = reqparse.RequestParser()
create_list_parser.add_argument("name")
create_list_parser.add_argument("description")

delete_list_parser = reqparse.RequestParser()
delete_list_parser.add_argument("mlistId")


class ListAPI(Resource):
    @marshal_with(list_out)
    @jwt_required()
    def post(self):
        if "cid" in session:
            tl = List.query.filter_by(Userl_id=session.get("cid")).all()
            if len(tl) < 4 :
                args = create_list_parser.parse_args()
                name = args.get("name")
                desc = args.get("description")

                if (len(name.strip()) > 0):
                    if (len(desc.strip()) > 0):
                        newList = List(List_name=name, List_desc=desc,
                                    Userl_id=session.get("cid"))
                        ADD.session.add(newList)
                        ADD.session.commit()
                        temp = List.query.filter_by(
                            Userl_id=session.get("cid"), List_name=name).first()
                        return temp
                    abort(400, message='List description should be String having length less than 100.')
                abort(400, message='List name should be String having length less than 20.')
            abort(400, message='you have exceeded the limit.')   
        abort(401, message='User login is required, please login to continue.')

    @jwt_required()
    def put(self, listId):
        if "cid" in session:
            temp = List.query.filter_by(
                Userl_id=session.get("cid"), List_id=listId).first()
            if temp is not None:
                args = create_list_parser.parse_args()
                lname = args.get("name")
                desc = args.get("description")

                if (len(lname.strip()) > 0):
                    if (len(desc.strip()) > 0):
                        temp.List_name = lname
                        temp.List_desc = desc
                        tem_card = Card.query.filter_by(Listc_id=listId).all()
                        for c in tem_card:
                            c.Card_list = lname
                        ADD.session.commit()
                        return 204
                    abort(400, message='List description should be String having length less than 100.')
                abort(400, message='List name should be String having length less than 20.')
            abort(404, message='List not found.')
        abort(401, message='User login is required, please login to continue.')

    @jwt_required()
    def delete(self, listId):
        if "cid" in session:
            temp = List.query.filter_by(
                Userl_id=session.get("cid"), List_id=listId).first()
            if temp is not None:
                args = delete_list_parser.parse_args()
                mlistId = args.get("mlistId")
                if mlistId != "":
                    mList = List.query.filter_by(
                        Userl_id=session.get("cid"), List_id=mlistId).first()
                    tem_card = Card.query.filter_by(Listc_id=listId).all()
                    for c in tem_card:
                        c.Card_list = mList.List_name
                        c.Listc_id = mList.List_id
                    List.query.filter_by(Userl_id=session.get(
                        "cid"), List_id=listId).delete()
                    ADD.session.commit()
                else:
                    List.query.filter_by(Userl_id=session.get(
                        "cid"), List_id=listId).delete()
                    Card.query.filter_by(Listc_id=listId).delete()
                    ADD.session.commit()
                return 200
            abort(404, message=errord["CE6"])
        abort(401, message='User login is required, please login to continue.')

    @marshal_with(list_out)
    @jwt_required()
    def get(self, listId):
        if "cid" in session:
            temp = List.query.filter_by(
                Userl_id=session.get("cid"), List_id=listId).first()
            return temp
        abort(401, message='User login is required, please login to continue.')

# ============================================ Dashboard API ================================================================
class DashAPI(Resource):
    @jwt_required()
    @cash.cached(timeout=5)
    def get(self):
        if "cid" in session:
            all = dict()
            temp = List.query.filter_by(Userl_id=session.get("cid")).all()
            for t in temp:
                newl = []
                newl.append(t.List_id)
                newl.append(t.List_name)
                newl.append(t.List_desc)
                newl.append([])
                tempc = Card.query.filter_by(Listc_id=t.List_id).all()
                if temp is not None:
                    for c in tempc:
                        if c.Card_dline < td and c.Card_status == "Pending":
                            c.Card_status = "Failed to complete"
                            c.Card_update_dt = td
                            ADD.session.commit()
                        newc = []
                        newc.append(c.Card_id)
                        newc.append(c.Card_title)
                        newc.append(c.Card_content)
                        newc.append(str(c.Card_dline))
                        newc.append(c.Card_status)
                        newl[3].append(newc)
                all[t.List_id] = newl
            return {'lister': all, 'user': session.get('cust'), 'td': td}
        abort(401, message='User login is required, please login to continue.')

# ============================================ Summary API ================================================================
class SummaryAPI(Resource):
    @jwt_required()
    def get(self):
        if "cid" in session:
            # download()
            lists = []

            temp_lists = List.query.filter_by(Userl_id=session.get("cid")).all()
            # Getting card info of every list
            for l in temp_lists:
                cards = Card.query.filter_by(Listc_id=l.List_id).all()
                # Collecting Cards by status
                complete_cards = Card.query.filter_by(Listc_id=l.List_id, Card_status='Completed').all()
                pending_cards = Card.query.filter_by(Listc_id=l.List_id, Card_status='Pending').all()
                dlpassed_cards = Card.query.filter_by(Listc_id=l.List_id, Card_status='Failed to complete').all()
                fname = l.List_name + str(l.List_id)
                # if len(complete_cards) >= 3:
                drange = {}
                for i in range(4,-1,-1):
                    drange[str(date.today()-timedelta(days = i))] = 0
                for c in complete_cards:
                    d = (c.Card_update_dt)[0:10]
                    drange[d] = drange[d] + 1
                dval = list(drange.values())
                dkeys = list(drange.keys())
                plt.clf()
                plt.plot(dkeys,dval)
                plt.ylabel('No of tasks')
                plt.title("Completed Task Trend")
                plt.savefig(f'static/images/{fname}tdline.PNG')

                total_cards = len(cards)
                comp_cards = len(complete_cards)
                pen_cards = len(pending_cards)
                dpass_cards = len(dlpassed_cards)

                # Graph ploting
                if total_cards > 0:
                    pdata = [comp_cards, pen_cards, dpass_cards]
                    pcolor = ['#089034', '#eda918', '#f00e2a']
                    plabel = ['Completed', 'Pending', 'Failed to complete']
                    plt.clf()
                    plt.bar(plabel, pdata, color=pcolor)
                    plt.ylabel('No of tasks')
                    plt.title("Task Status Bar")
                    plt.savefig(f'static/images/{fname}.PNG')
                
                if len(cards) > 0:
                    lists.append([l.List_name, total_cards, comp_cards, pen_cards, dpass_cards, fname])

            twho = Card.query.filter_by(UserC_id = session.get('cid')).all()
            if len(twho) > 0:
                u = session.get('cust')
                completecards = Card.query.filter_by(UserC_id = session.get('cid'), Card_status='Completed').all()
                pendingcards = Card.query.filter_by(UserC_id = session.get('cid'), Card_status='Pending').all()
                dlpassedcards = Card.query.filter_by(UserC_id = session.get('cid'), Card_status='Failed to complete').all()
                # if len(complete_cards) >= 3:
                # drange = {}
                # for i in range(4,-1,-1):
                #     drange[str(date.today()-timedelta(days = i))] = 0
                for c in completecards:
                    d = (c.Card_update_dt)[0:10]
                    drange[d] = drange[d] + 1
                dval = list(drange.values())
                dkeys = list(drange.keys())
                plt.clf()
                plt.plot(dkeys,dval)
                plt.ylabel('No of tasks')
                plt.title("Completed Task Trend")
                plt.savefig(f'static/images/{u}tdline.PNG')
                
                if len(twho) > 0:
                    pdata = [len(completecards), len(pendingcards), len(dlpassedcards)]
                    pcolor = ['#089034', '#eda918', '#f00e2a']
                    plabel = ['Completed', 'Pending', 'Failed to complete']
                    plt.clf()
                    plt.bar(plabel, pdata, color=pcolor)
                    plt.ylabel('No of tasks')
                    plt.title("Task Status Bar")
                    plt.savefig(f'static/images/{u}.PNG')

                lists.append(["Dashboard", len(twho), len(completecards), len(pendingcards), len(dlpassedcards), u])
            # print(lists)
            return {'lister': lists, 'user': session.get('cust')}
        abort(401, message='User login is required, please login to continue.')


# ============================================ Export API ================================================================
class ExportAPI(Resource):
    @jwt_required()
    def get(self):
        if "cid" in session:
            usern = session.get("cust")
            userm = (User.query.filter_by(User_id = session.get("cid")).first()).User_email
            lis = []
            car = []
            temp = List.query.filter_by(Userl_id = session.get("cid")).all()
            if len(temp) > 0:
                for t in temp:
                    newl = []
                    # newl.append(t.List_id)
                    newl.append(t.List_name)
                    newl.append(t.List_desc)
                    lis.append(newl)

            tempc = Card.query.filter_by(UserC_id = session.get("cid")).all()
            if len(tempc) > 0:
                for c in tempc:
                    if c.Card_dline < td and c.Card_status == "Pending":
                        c.Card_status = "Failed to complete"
                        c.Card_update_dt = td
                        ADD.session.commit()
                    newc = []
                    # newc.append(c.Card_id)
                    newc.append(c.Card_list)
                    newc.append(c.Card_title)
                    newc.append(c.Card_content)
                    newc.append(c.Card_create_dt)
                    newc.append(str(c.Card_dline))
                    newc.append(c.Card_update_dt)
                    newc.append(c.Card_status)
                    car.append(newc)

            testport = applications.tasks.exporter(lisd=lis,cars=car, rmail=userm, user=usern)
        return "User not found!"


# ============================================ Card API ================================================================
card_out = {
    "Card_id": fields.Integer,
    "Listc_id": fields.Integer,
    "Card_list": fields.String,
    "Card_title": fields.String,
    "Card_content": fields.String,
    "Card_dline": fields.DateTime,
    "Card_status": fields.String
}

create_card_parser = reqparse.RequestParser()
create_card_parser.add_argument("title")
create_card_parser.add_argument("content")
create_card_parser.add_argument("deadline")
create_card_parser.add_argument("status")

update_card_parser = reqparse.RequestParser()
update_card_parser.add_argument("list")
update_card_parser.add_argument("title")
update_card_parser.add_argument("content")
update_card_parser.add_argument("deadline")
update_card_parser.add_argument("status")


class CardAPI(Resource):
    @jwt_required()
    def post(self, listId):
        if "cid" in session:
            temp = List.query.filter_by(
                Userl_id=session.get("cid"), List_id=listId).first()
            if temp is not None:
                args = create_card_parser.parse_args()
                title = args.get("title")
                content = args.get("content")
                d = args.get("deadline")
                status = args.get("status")

                d1 = d.replace('T', ' ')

                if status == "True":
                    status = "Completed"
                elif status == "" or status == "False":
                    status = "Pending"

                if (len(title.strip()) > 0):
                    if (len(content.strip()) > 0):
                        if status in statusList:
                            newCard = Card(Card_list=temp.List_name,
                                           Card_title=title,
                                           Card_content=content,
                                           Card_update_dt=td,
                                           Card_dline=d1,
                                           UserC_id=session.get("cid"),
                                           Listc_id=listId,
                                           Card_status=status)

                            ADD.session.add(newCard)
                            ADD.session.commit()
                            return 201
                        abort(400, message='Card status [Pending, Completed, Failed to complete] is required.')
                    abort(400, message='Card content should be String having length less than 100.')
                abort(400, messagg='Card name should be String having length less than 20.')
            abort(404, message='List not found.')
        abort(401, message='User login is required, please login to continue.')

    @marshal_with(card_out)
    @jwt_required()
    def put(self, cardId):
        if "cid" in session:
            tempc = Card.query.filter_by(
                UserC_id=session.get("cid"), Card_id=cardId).first()
            if tempc is not None:
                args = update_card_parser.parse_args()
                mlist = args.get("list")
                title = args.get("title")
                content = args.get("content")
                d = args.get("deadline")
                status = args.get("status")
                d1 = d.replace('T', ' ')

                if status == "True":
                    status = "Completed"
                elif status == "" or status == "False":
                    status = "Pending"
                tempm = List.query.filter_by(
                    Userl_id=session.get("cid"), List_id=mlist).first()

                if tempm is not None:
                    if (len(title.strip()) > 0):
                        if (len(content.strip()) > 0):
                            if status in statusList:
                                tempc.Card_list = tempm.List_name
                                tempc.Card_title = title
                                tempc.Card_content = content
                                tempc.Card_dline = d1
                                tempc.Card_update_dt = td
                                tempc.Listc_id = tempm.List_id
                                tempc.Card_status = status
                                ADD.session.commit()
                                return 204
                            abort(400, message='Card status [Pending, Completed, Failed to complete] is required.')
                        abort(400, message='Card content should be String having length less than 100.')
                    abort(400, messagg='Card name should be String having length less than 20.')
                abort(404, message='List not found.')
            abort(404, message='Card not found.')
            # abort(404, message=errord["DE8"])
        abort(401, message='User login is required, please login to continue.')

    @jwt_required()
    def delete(self, cardId):
        if "cid" in session:
            tempc = Card.query.filter_by(
                UserC_id=session.get("cid"), Card_id=cardId).first()
            if tempc is not None:
                Card.query.filter_by(Card_id=cardId).delete()
                ADD.session.commit()
                return 200
            abort(404, message='Card not found.')
        abort(401, message='User login is required, please login to continue.')

    @jwt_required()
    def get(self, cardId):
        if "cid" in session:
            temp = Card.query.filter_by(
                UserC_id=session.get("cid"), Card_id=cardId).first()
            if temp is not None:
                if temp.Card_status == 'Pending':
                    st = ""
                    return {
                        "Card_id": temp.Card_id,
                        "Listc_id": temp.Listc_id,
                        "Card_list": temp.Card_list,
                        "Card_title": temp.Card_title,
                        "Card_content": temp.Card_content,
                        "Card_dline": temp.Card_dline,
                        "Card_status": st,
                        "td": td
                    }
                return {
                    "Card_id": temp.Card_id,
                    "Listc_id": temp.Listc_id,
                    "Card_list": temp.Card_list,
                    "Card_title": temp.Card_title,
                    "Card_content": temp.Card_content,
                    "Card_dline": temp.Card_dline,
                    "Card_status": temp.Card_status,
                    "td": td
                }
            abort(404, message='Card not found.')
        abort(401, message='User login is required, please login to continue.')


@jwt_required()
@capp.route('/export')
def exporterd():
    if "cid" in session:
        user = session.get("cust")
        lis = []
        car = []
        temp = List.query.filter_by(Userl_id = session.get("cid")).all()
        if len(temp) > 0:
            for t in temp:
                newl = []
                # newl.append(t.List_id)
                newl.append(t.List_name)
                newl.append(t.List_desc)
                lis.append(newl)

        tempc = Card.query.filter_by(UserC_id = session.get("cid")).all()
        if len(tempc) > 0:
            for c in tempc:
                if c.Card_dline < td and c.Card_status == "Pending":
                    c.Card_status = "Failed to complete"
                    c.Card_update_dt = td
                    ADD.session.commit()
                newc = []
                # newc.append(c.Card_id)
                newc.append(c.Card_list)
                newc.append(c.Card_title)
                newc.append(c.Card_content)
                newc.append(c.Card_create_dt)
                newc.append(str(c.Card_dline))
                newc.append(c.Card_update_dt)
                newc.append(c.Card_status)
                car.append(newc)

        lis_fields = ['List Name', 'List Description'] 
        car_fields = ['List Name', 'Card Title', 'Content', 'Create Date', 'Deadline', 'Updated At', 'Status'] 

        fname = f'static/{user}_details.csv'

        with open(fname, 'w', newline='', encoding='utf8') as csvf: 
        # creating a csv writer object 
            cwriter = csv.writer(csvf) 
            cwriter.writerow(lis_fields) 
            cwriter.writerows(lis)
            cwriter.writerow(car_fields) 
            cwriter.writerows(car)
        return send_from_directory("static",f'{user}_details.csv')
    return 'User login is required, please login to continue.'

@capp.route('/testc')
@cash.cached(timeout=50)
def testingcache():
    time.sleep(10)
    return "Cached"


class DetailsAPI(Resource):
    def get(self):
        mailList = []
        users = User.query.all()
        for u in users:
            mailList.append(u.User_email)
        # print(users) 
        return mailList

