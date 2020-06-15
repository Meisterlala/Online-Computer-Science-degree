from flask import Flask, render_template, request, redirect
from cs50 import SQL

app = Flask(__name__)


@app.route("/")
def index():
    db = SQL("sqlite:///lecture.db")
    rows = db.execute("SELECT * FROM registrants")
    return render_template("index.html", rows=rows)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        db = SQL("sqlite:///lecture.db")
        name = request.form.get("name")
        email = request.form.get("email")
        db.execute(
            "INSERT INTO registrants (name, email) VALUES (:name, :email)", name=name, email=email)
        return redirect("/")
