from flask import Flask, request, render_template, redirect as redirect_response, Response
from json import dumps as serialize
import os
from datetime import datetime
from time import sleep
from pprint import pformat
from secrets import token_urlsafe as token_b64
from datetime import datetime, timedelta

from db import DatabaseService, PoolConfig, ConnectionConfig


def now():
    return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")


BASE_URL = os.environ["BASE_URL"]
DB_USERNAME = os.environ["DATABASE_USERNAME"]
DB_PASSWORD = os.environ["DATABASE_PASSWORD"]
DB_DATABASE = os.environ["DATABASE_DB"]
DB_TABLE = os.environ["DATABASE_TABLE"]
DB_SERVER = os.environ["DATABASE_HOST"]
ACCESS_KEY = os.environ["ACCESS_KEY"]

COOKIE_PREFIX = BASE_URL.replace(".", "_")
SESSION_COOKIE_KEY = COOKIE_PREFIX+"__session"

db = DatabaseService(
    poolConfig=PoolConfig(2, 3),
    connectionConfig=ConnectionConfig(
        db=DB_DATABASE,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_SERVER,
    ))

app = Flask(__name__)


@app.route("/", methods=["get"])
def index():
    session_cookie = request.cookies.get(SESSION_COOKIE_KEY)
    if session_cookie is None:
        return redirect_response("/login")
    return "Welcome to /"


@app.route("/login", methods=["get"])
def login_page():
    return render_template("authenticate.html.j2", method="post", action="/login", failed=False)


@app.route("/login", methods=["post"])
def login_request():
    username, password = request.form["username"], request.form["password"]
    user_id = db.users.authenticate(username, password)

    if user_id is None:
        return render_template("authenticate.html.j2", method="post", action="/login", failed=True)

    # Auth success
    persist_session = request.form.get("persist_session", False)

    if persist_session:
        expiry = datetime.utcnow() + timedelta(days=30)
    else:
        expiry = datetime.utcnow() + timedelta(days=1)

    session_token = token_b64(64)

    db.sessions.create(token=session_token,
                       user_id=user_id, expire_time=expiry)

    next = request.args.get("next", "/")
    response = redirect_response(next)
    response.set_cookie(SESSION_COOKIE_KEY,
                       session_token, expires=expiry)
    return response


@app.route("/<path:path>", methods=["get"])
def redirect(path):
    print("redirect endpoint hit")
    try:
        target = db.redirects.get_active_target(path)
    except Exception as e:
        print("exception", e)
        raise
        return redirect_response("https://" + BASE_URL)
    if target is None:
        return "Oops!"
    return redirect_response(target)
