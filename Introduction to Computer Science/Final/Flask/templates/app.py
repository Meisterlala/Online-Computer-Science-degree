from flask import Flask, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

Session(app)


@app.route("/")
def index():
    return render_template("index.html")
