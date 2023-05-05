# # ==================================================== Imports ====================================================================
# # import models
# from flask import render_template
# from flask import current_app as capp
# from datetime import date
# import matplotlib 
# from applications.models import ADD ,User, Card, List
# matplotlib.use('Agg')
# from matplotlib import pyplot as plt
# import redis
# from datetime import datetime
# from jinja2 import Template

# import smtplib
# from email.message import EmailMessage

# # from celery import Celery
# from celery.schedules import crontab

# from applications.workers import celery

# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# ctd = str(date.today())

# # -------------------------------------------------------------------
# def reportGenrator(temFile, d, usern):
#     with open(temFile) as fileTemp:
#         t = Template(fileTemp.read())
#         return t.render(data=d, username=usern)



# # -------------------------------------------------------------------
# # def make_celery(capp):
# #     celery = Celery(
# #         capp.import_name,
# #         backend=capp.config['CELERY_RESULT_BACKEND'],
# #         broker=capp.config['CELERY_BROKER_URL']
# #     )
# #     celery.conf.update(capp.config)

# #     class ContextTask(celery.Task):
# #         def __call__(self, *args, **kwargs):
# #             with capp.app_context():
# #                 return self.run(*args, **kwargs)

# #     celery.Task = ContextTask
# #     return celery
# # # -------------------------------------------------------------------
# # capp.config.update(
# #     CELERY_BROKER_URL='redis://localhost:6379',
# #     CELERY_RESULT_BACKEND='redis://localhost:6379'
# # )
# # # -------------------------------------------------------------------
# # celery = make_celery(capp)
# # capp.app_context().push() 
# # capp.init(celery)

# SMTP_SERVER_HOST= "localhost"
# SMTP_SERVER_PORT= 1025
# SENDER_ADDRESS = "dev@gmail.com"
# SENDER_PASSWORD = ""

# # -------------------------------------------------------------------
# def send_email(to_address, subject,message):
#     msg=MIMEMultipart()
#     msg["From"] = SENDER_ADDRESS
#     msg["To"] = to_address
#     msg["Subject"] = subject

#     msg.attach(MIMEText(message,"html"))
    
#     s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
#     s.login(SENDER_ADDRESS,SENDER_PASSWORD)

#     s.send_message(msg)
#     s.quit()
#     return True

# # -------------------------------------------------------------------
# @celery.task()
# def just_say_hello():
#     print("inside Task")
#     print("hello " )
#     return "name"
# # -------------------------------------------------------------------



# # @celery.task
# # def deadlineReminder():
# #     users=[
# #         {"name":"raj", "email":"raj@gmail.com"},
# #         {"name":"maan","email":"maan@gmail.com"}
# #     ]
# #     for i in users:
# #         send_email(i["email"], subject="Hello", message="welcom to the new world")
# #     return True

# users = User.query.all()
# print(users)
# def getmail():
#     mail_list = []
#     users = User.query.all()
#     print(users)
#     for u in users:
#         print("3hellooo")
#         dcard = Card.query.filter_by(UserC_id = u.User_id).all()
#         print("4hellooo")
#         for c in dcard:
#             print("5helloo")
#             if c.Card_status == 'Pending' and ctd in c.Card_dline:
#                 print("6helloo")
#                 mail_list.append(u.User_email)
#     return mail_list

# @celery.task
# def deadlineReminder():
#     tempm = getmail()
#     print(users)
#     for m in tempm:
#          send_email(m, subject="Task Deadline Reminder", message="You have some pending tasks!")
#     print("1helloo")
#     # # users = User.query.all()
#     # print(users)
#     # print("2hellooooooooooooooooooooooooooo")
#     # for u in users:
#     #     print("3hellooooooooooooooooooooooooooo")
#     #     dcard = Card.query.filter_by(UserC_id = u.User_id).all()
#     #     print("4hellooooooooooooooooooooooooooo")
#     #     for c in dcard:
#     #         print("5hellooooooooooooooooooooooooooo")
#     #         if c.Card_status == 'Pending' and ctd in c.Card_dline:
#     #             print("6hellooooooooooooooooooooooooooo")
#     #             send_email(u.User_email, subject="Task Deadline Reminder", message="You have some pending tasks!")
#     return "Daily reminder done!"


# @celery.task
# def monthReport():  
#     for u in users:
#         temp = List.query.filter_by(Userl_id=u.User_id).all()
#         if temp is not None:
#             all = []
#             for t in temp:
#                 newl = []
#                 newl.append(t.List_name)
#                 newl.append(t.List_desc)
#                 newl.append([])
#                 tempc = Card.query.filter_by(Listc_id=t.List_id).all()
#                 if tempc is not None:
#                     for c in tempc:
#                         if (c.Card_create_dt )[0:9] == ctd[0:9]:
#                             newc = []
#                             newc.append(c.Card_id)
#                             newc.append(c.Card_title)
#                             newc.append(c.Card_content)
#                             newc.append(str(c.Card_dline))
#                             newc.append(c.Card_status)
#                             newl[3].append(newc)
#             all.append(newl)
#         # pdfGenrator(user=u.User_name, uId=u.User_id, data=all)
#         send_email(u.User_email, subject="KanBan-Monthly Progress Report", message = "message")
#     return "Monthly Reports Sent!"    

# @celery.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('deadlineReminder') every 10 seconds.
#     sender.add_periodic_task(10.0, deadlineReminder.s(), name='DeadlineReminder')

#     # Calls test('monthReport') every 30 seconds
#     # sender.add_periodic_task(30.0, monthReport.s(), expires=10)
    
# @capp.route("/hello", methods=["GET","POST"])
# def hello():
#     job = just_say_hello.delay()
#     # result = job.wait()
#     return str((users[0]).User_name), 200

# # ==================================================== Main Route : Home Page ====================================================
# @capp.route('/')
# def Welcome():
#     return render_template("index.html")

# # users = User.query.all()
# # print(users)

    # tempm = getmail()
    # print(users)
    # for m in tempm:
    #      send_email(m, subject="Task Deadline Reminder", message="You have some pending tasks!")
    # print("1helloo")




# from celery import Celery
# from applications.workers import celery
# from flask import current_app as capp

# def make_celery(capp):
#     celery = Celery(
#         capp.import_name,
#         backend=capp.config['CELERY_RESULT_BACKEND'],
#         broker=capp.config['CELERY_BROKER_URL']
#     )
#     celery.conf.update(capp.config)
#     print("hello000")
#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with capp.app_context():
#                 return self.run(*args, **kwargs)
#     print("hello000")
#     celery.Task = ContextTask
#     return celery
# # -------------------------------------------------------------------
# capp.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379',
#     CELERY_RESULT_BACKEND='redis://localhost:6379'
# )
# # -------------------------------------------------------------------
# celery = make_celery(capp)