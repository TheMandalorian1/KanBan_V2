# ====================== Imports ===================================================
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

# Creating a Database instance
ADD = SQLAlchemy()

#Creating Models
class User(ADD.Model):
    User_id = Column(Integer, primary_key = True, autoincrement = True)
    User_name = Column(String(30), nullable = False)
    User_email = Column(String(100), nullable = False, unique = True)
    User_pass = Column(String(15), nullable = False)
    lists = relationship("List", backref="custom")
    cards = relationship("Card", backref="tasks")

class List(ADD.Model):
    List_id = Column(Integer, primary_key = True, autoincrement = True)
    List_name = Column(String(20), nullable = False)
    List_desc = Column(String(100), nullable = False)
    Userl_id = Column(Integer, ForeignKey("user.User_id"), nullable = False)
    cards = relationship("Card", backref="task")

class Card(ADD.Model):
    Card_id = Column(Integer, primary_key = True, autoincrement = True) 
    Card_list = Column(String(20), nullable = False)
    Card_title = Column(String(20), nullable = False)
    Card_content = Column(String(100), nullable = False)
    Card_create_dt = Column(String(16), default = str(date.today()))
    Card_update_dt = Column(String(16), default = datetime.now().strftime("%Y-%m-%d %H:%M"))
    #card deadline status : 
    Card_status = Column(String(30), nullable = False)
    Card_dline = Column(String(16), nullable = False)
    UserC_id = Column(Integer, ForeignKey("user.User_id"), nullable = False)
    Listc_id = Column(Integer, ForeignKey("list.List_id"), nullable = False)