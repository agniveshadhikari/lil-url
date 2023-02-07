from flask import Flask, request, render_template, redirect as redirect_response, Response, g as request_context
import os
from datetime import datetime
from secrets import token_urlsafe as token_b64
from datetime import datetime, timedelta

from db import DatabaseService, PoolConfig, ConnectionConfig


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
    poolConfig=PoolConfig(3, 5),
    connectionConfig=ConnectionConfig(
        db=DB_DATABASE,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_SERVER,
    ))

app = Flask(__name__)


@app.before_request
def populate_request_context():
    session_token = request.cookies.get(SESSION_COOKIE_KEY)
    user = db.sessions.get_user(session_token)
    if user is None and request.path in ["/"]:
        return redirect_response(f"/login?next={request.path}")

    request_context.user = user


@app.route("/favicon.ico")
def ignore():
    return ""


def render_index(user=None):
    if user is None:
        user = request_context.user

    redirects = db.redirects.get_all(user_id=user.id)

    return render_template("manage.html.j2", user=user, redirects=redirects, base_url=BASE_URL)


@app.route("/", methods=["get"])
def index():
    return render_index()


@app.route("/", methods=["post"])
def action():
    action = request.form.get("action")
    if action == "create":
        return create()
    elif action == "delete":
        return delete()
    else:
        return Response(f"Invalid action {action}", 400)


def create():
    path, target = request.form.get("path"), request.form.get("target")
    user = request_context.user

    db.redirects.create(path, target, user.id)

    return render_index()


def delete():
    path = request.form.get("path")
    if path is None:
        return Response("Can't delete path None", 400)

    db.redirects.delete(path)

    return render_index()


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
        return redirect_response("https://" + BASE_URL)
    if target is None:
        return "Oops!"
    return redirect_response(target)
