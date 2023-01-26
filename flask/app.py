from flask import Flask, request, render_template, redirect as redirect_response, Response
from json import dumps as serialize
import  psycopg2
import os
from datetime import datetime
from time import sleep
from pprint import pformat
def now():
    return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")


BASE_URL = os.environ["BASE_URL"]
DB_USERNAME = os.environ["DATABASE_USERNAME"]
DB_PASSWORD = os.environ["DATABASE_PASSWORD"]
DB_DATABASE = os.environ["DATABASE_DB"]
DB_TABLE = os.environ["DATABASE_TABLE"]
DB_SERVER = os.environ["DATABASE_HOST"]
ACCESS_KEY = os.environ["ACCESS_KEY"]


app = Flask(__name__)

conn = None

def get_cursor():
    if conn is None or conn.closed:
        conn = psycopg2.connect(
            dbname=DB_DATABASE,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_SERVER,
            sslmode="require")

        conn.autocommit = True
    
    return conn.cursor()




@app.route("/")
def index():

    # If not logged in
    if False:
        return redirect("/login")


    return render_template("home.html.j2", method="post", action="/login")

@app.route("/login" methods="get")
def get_login():
    if request.form.get('accessKey') != ACCESS_KEY:
        return render_template("authenticate.html.j2", method="post", action="/login")

@app.route("/create", methods=["get"])
def create_get():
    return render_template("create.html")

@app.route("/create", methods=["post"])
def create_post():
    if request.form['accessKey'] != ACCESS_KEY:
        return Response("Incorrect access key", 401)

    result = db_insert(request.form['slug'], request.form['target'])
    if result:
        return render_template("created.html.j2", url=BASE_URL+"/"+request.form["slug"])
    else:
        return "Oops!"

@app.route("/manage", methods=['get', 'post'])
def manage():
    if request.form.get('accessKey') != ACCESS_KEY:
        return render_template("authenticate.html.j2", method="post", action="/manage")
    
    return render_template("manage.html.j2", redirects=db_list())

@app.route("/<string:slug>", methods=["get"])
def redirect(slug):
    target = db_lookup(slug)
    if target is None:
        return "Oops!"
    return redirect_response(target)

def db_insert(slug, target):
    curs = get_cursor()
    try:
        curs.execute("insert into redirect values(%s, %s)", (slug, target))
        return True
    except:
        return False

def db_lookup(slug):
    curs = get_cursor()
    curs.execute("select target from redirect where slug=%s", (slug,))
    result = curs.fetchone()
    if result is None:
        return None
    target, = result
    return target
    
def db_list():
    curs = get_cursor()
    curs.execute("select * from redirect")
    return curs.fetchall()