# to create virtualenv using windows command promt
- change directory `cd`+ project_folder path
- to create virtualenv `python3 -m venv .proj-env`
- to activate virtualenv `.proj-env\Scripts\activate.bat`

# to intall required packages-
- to install all packages `pip install -r requirements.txt`
# to run the application -
- `python main.py`
## start redis server on windows
sudo service redis-server start

redis-server

## start worker in ubuntu
celery -A main.celery worker -l info

## start beat in windows
celery -A main.celery beat --max-interval 1 -l info

## mailhog server
```http://127.0.0.1:5000:8025```

# Folder Structure
- `application` is where our application code is.
- `static` - default `static` files folder and has CSS files. 
- `static/images` has all the images.
- `static/components` has all the js components.
- `templates` - Default flask templates folder
- `documents` has yaml file for API and project report pdf.


```
/
├── __pycache__/
│   └── main.cpython-38.pyc
├── addDB.sqlite3
├── applications/
│   ├── __init__.py
│   ├── __pycache__/
│   │   ├── __init__.cpython-310.pyc
│   │   ├── __init__.cpython-38.pyc
│   │   ├── api.cpython-310.pyc
│   │   ├── api.cpython-38.pyc
│   │   ├── app.cpython-310.pyc
│   │   ├── app.cpython-38.pyc
│   │   ├── mailer.cpython-310.pyc
│   │   ├── mailer.cpython-38.pyc
│   │   ├── models.cpython-310.pyc
│   │   ├── models.cpython-38.pyc
│   │   ├── tasks.cpython-310.pyc
│   │   ├── tasks.cpython-38.pyc
│   │   ├── workers.cpython-310.pyc
│   │   └── workers.cpython-38.pyc
│   ├── api.py
│   ├── mailer.py
│   ├── models.py
│   ├── tasks.py
│   ├── tempCodeRunnerFile.py
│   ├── test.py
│   └── workers.py
├── celerybeat-schedule
├── commands.txt
├── dump.rdb
├── instance/
│   └── addDB.sqlite3
├── main.py
├── Project Report.pdf
├── readme.md
├── requirements.txt
├── static/
│   ├── Aditya_details.csv
│   ├── app.js
│   ├── components/
│   │   ├── addcard.js
│   │   ├── addlist.js
│   │   ├── dashboard.js
│   │   ├── deletecard.js
│   │   ├── deletelist.js
│   │   ├── editcard.js
│   │   ├── editlist.js
│   │   ├── login.js
│   │   ├── register.js
│   │   └── summary.js
│   ├── images/
│   │   ├── Aditya.PNG
│   │   ├── Aditya2.PNG
│   │   ├── Aditya4.PNG
│   │   ├── Aditya4tdline.PNG
│   │   ├── Adityatdline.PNG
│   │   ├── favicon.ico
│   │   ├── List-11.PNG
│   │   ├── List-111.PNG
│   │   ├── List-13.PNG
│   │   ├── List-13tdline.PNG
│   │   ├── List-22.PNG
│   │   ├── List17.PNG
│   │   ├── List17tdline.PNG
│   │   └── vf5.PNG
│   ├── List1_details.csv
│   ├── style.css
│   └── styles.css
├── tempCodeRunnerFile.py
└── templates/
    ├── indeed.html
    ├── index.html
    └── reporter.html

```