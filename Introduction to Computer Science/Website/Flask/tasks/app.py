from flask import Flask, render_template, request, redirect


app = Flask(__name__)

todos = []


@app.route("/")
def task():
    return render_template("task.html", todos=todos)


@app.route("/add", methods=["GET", "POST"])
def bye():
    if request.method == "GET":
        return render_template("add.html")
    else:
        todo = request.form.get("name")
        todos.append(todo)
        return redirect("/")
