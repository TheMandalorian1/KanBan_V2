from applications.models import User, List, Card, ADD
from flask import current_app as capp
from flask import render_template
from datetime import date
from jinja2 import Template
# from weasyprint import HTML
import csv
from celery.schedules import crontab
from applications.workers import celery

from applications.mailer import sendMail, sendMemer

ctd = str(date.today())

# celery = celery
# capp.app_context().push()
# celery.conf.update(
#      broker_url='redis://localhost:6379',
#      result_backend='redis://localhost:6379'
#  )
# celery.Task = ContextTask
# capp.app_context().push()
# capp.config['CELERY_BROKER_URL'] = "redis://localhost:6379"
# capp.config['CELERY_RESULT_BACKEND'] = "redis://localhost:6379"
# capp.app_context().push()

def reportGenrator(temFile, d, usern):
    with open(temFile) as fileTemp:
        t = Template(fileTemp.read())
        return t.render(lister=d, username=usern)

# def pdfGenrator(user, uId, data):
#     msg = reportGenrator("templates/reporter.html", data)
#     html = HTML(string=msg)
#     fname = str(user)+".pdf"
#     html.write_pdf(target=fname)
#     return fname

@celery.task()
def exporter(lisd, cars, rmail, user):
    fname = f'static/{user}_details.csv'

    lis_fields = ['List Name', 'List Description'] 
    car_fields = ['List Name', 'Card Title', 'Content', 'Create Date', 'Deadline', 'Updated At', 'Status']

    with open(fname, 'w', newline='', encoding='utf8') as csvf: 
    # creating a csv writer object 
        cwriter = csv.writer(csvf) 
        cwriter.writerow(lis_fields) 
        cwriter.writerows(lisd)
        cwriter.writerow(car_fields) 
        cwriter.writerows(cars)

    filenum = str(user) + '_details.csv'
    sendMemer(reciever=rmail, subject="CSV Mail", message= "This is a csv mail.", attachment=f'static/{user}_details.csv')
    return "CSV file exported!"


@celery.task()
def just_say_hello():
    users=[
        {"name":"aditya", "email":"aditya@gmail.com"},
        {"name":"anand","email":"anand@gmail.com"}
    ]
    for u in users:
        rm = u.get("email")
        sendMail(rm, subject="Task Deadline Reminder", message="You have some pending tasks!")
    print("inside Task")
    return "Daily reminder done!"



@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):

    # Calls test('deadlineReminder') every 10 seconds.
    # sender.add_periodic_task(10.0, just_say_hello.s(), name='just_say_hello')

    # Calls deadlineReminder.s() daily.
    sender.add_periodic_task(10, deadlineReminder.s(), name='DeadlineReminder') 
    # Calls monthReport.s() on 1st day of the month.
    sender.add_periodic_task(10, monthReport.s(), name='MonthReport')

@celery.task
def deadlineReminder():
    users = User.query.all()
    print(users)
    for u in users:
        dcard = Card.query.filter_by(UserC_id = u.User_id, Card_status = 'Pending').all()
        # for c in dcard:
        #     if c.Card_status == 'Pending' and ctd in c.Card_dline:
        if len(dcard) > 0:
            rmail = u.User_email
            sendMail(rmail, subject="Task Deadline Reminder", message="You have some pending tasks!")
    return "Daily reminder done!"

@celery.task
def monthReport(): 
    users = User.query.all() 
    for u in users:
        usern = u.User_name
        umail = u.User_email
        temp = List.query.filter_by(Userl_id=u.User_id).all()
        if temp is not None:
            all = []
            for t in temp:
                newl = []
                newl.append(t.List_name)
                newl.append(t.List_desc)
                newl.append([])
                tempc = Card.query.filter_by(Listc_id=t.List_id).all()
                if tempc is not None:
                    for c in tempc:
                        if (c.Card_create_dt )[0:9] == ctd[0:9]:
                            newc = []
                            newc.append(c.Card_id)
                            newc.append(c.Card_title)
                            newc.append(c.Card_content)
                            newc.append(str(c.Card_dline))
                            newc.append(c.Card_status)
                            newl[2].append(newc)
            all.append(newl)

        mesage = reportGenrator("templates/reporter.html", all, usern)
        sendMail(umail, subject="KanBan-Monthly Progress Report", message = mesage)
    return "Monthly Reports Sent!"  




@celery.task()
def hello():
    # sendMail(reciever='add@gmail.com', subject="Tester Mail", message="This is a test mail.")
    sendMemer(reciever='add@gmail.com', subject="CSV Mail", message="This is a test mail.", attachment='./static/Aditya_details.csv')

    return str("(job)"), 200


@capp.route('/')
def Welcome():
    return render_template("index.html")