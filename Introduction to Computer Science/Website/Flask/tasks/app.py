from flask import Flask, render_template, request, redirect, session,  url_for
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def task():
    if "todos" not in session:
        session["todos"] = []
    return render_template("task.html", todos=session["todos"])


@app.route("/add", methods=["GET", "POST"])
def bye():
    if request.method == "GET":
        return render_template("add.html")
    else:
        todo = request.form.get("name")
        t = session.get("todos")
        t.append(todo)
        session.modified = True
        return redirect("/")
