import os
import datetime
import re

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from decimal import Decimal

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


"""
# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")
"""


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    db = SQL("sqlite:///finance.db")
    money = db.execute("SELECT cash FROM users where id=:id",
                       id=session["user_id"])[0]["cash"]
    totalvalue = money

    transactions = db.execute("SELECT symbol, amount FROM history where userid=:id",
                              id=session["user_id"])

    temp = {}
    for t in transactions:
        if t["symbol"] in temp:
            temp[t["symbol"]] += int(t["amount"])
        else:
            temp[t["symbol"]] = int(t["amount"])

    display = []
    for e in temp:
        data = lookup(e)
        entry = {}
        entry["name"] = data["name"]
        entry["price"] = usd(data["price"])
        entry["amount"] = temp[e]

        val = float(data["price"]) * int(temp[e])
        totalvalue += val
        entry["value"] = usd(val)

        display.append(entry)

    return render_template("index.html", balance=usd(money), value=usd(totalvalue), entrys=display)


@ app.route("/buy", methods=["GET", "POST"])
@ login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    symbol = request.form.get("symbol")
    shares = request.form.get("shares")

    if not symbol:
        return apology("must provide Symbol", 403)
    if not shares:
        return apology("must provide shares", 403)
    if int(shares) <= 0:
        return apology("enter positive int", 403)

    data = lookup(symbol)
    price = data["price"]

    db = SQL("sqlite:///finance.db")
    money = db.execute("SELECT cash FROM users where id=:id",
                       id=session["user_id"])[0]["cash"]

    if (price * int(shares)) > money:
        return apology("Your to poor", 403)

    restmoney = money - (price * int(shares))
    db.execute("UPDATE users SET cash = :mon WHERE id = :id",
               mon=restmoney,
               id=session["user_id"])

    db.execute("INSERT INTO history (userid, symbol, amount, price, date) VALUES (:u, :s, :a, :p, :d)",
               u=session["user_id"],
               s=symbol,
               a=shares,
               p=price,
               d=datetime.datetime.now())
    return redirect("/")


@ app.route("/history")
@ login_required
def history():
    db = SQL("sqlite:///finance.db")

    transactions = db.execute("SELECT * FROM history where userid=:id",
                              id=session["user_id"])

    display = []
    for e in transactions:
        data = lookup(e["symbol"])
        entry = {}
        entry["name"] = data["name"]
        entry["price"] = usd(e["price"])
        entry["amount"] = e["amount"]
        entry["symbol"] = e["symbol"]
        entry["date"] = e["date"]

        display.append(entry)

    return render_template("history.html", entrys=display)


@ app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Configure CS50 Library to use SQLite database
        db = SQL("sqlite:///finance.db")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@ app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@ app.route("/quote", methods=["GET", "POST"])
@ login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    symbol = request.form.get("symbol")
    if not symbol:
        return apology("must provide symbol", 403)

    data = lookup(symbol)
    return render_template("quoted.html", entry=data)


@ app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")
    else:

        # Configure CS50 Library to use SQLite database
        db = SQL("sqlite:///finance.db")

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 403)
        if not password:
            return apology("must provide password", 403)
        if not confirmation:
            return apology("must confirm password", 403)
        if password != confirmation:
            return apology("passwords dont match", 403)

        if len(password) < 8:
            return apology("password to short", 403)
        if re.search("[0-9]", password) is None:
            return apology("Please include a Number", 403)

        hash = generate_password_hash(password)
        db.execute(
            "INSERT INTO users (username, hash) VALUES (:u, :h);", u=username, h=hash)

        return redirect("/login")


@ app.route("/sell", methods=["GET", "POST"])
@ login_required
def sell():
    """Sell shares of stock"""
    db = SQL("sqlite:///finance.db")
    if request.method == "GET":

        stocks = db.execute("SELECT DISTINCT symbol FROM history where userid=:id",
                            id=session["user_id"])

        return render_template("sell.html", options=stocks)

    shares = request.form.get("shares")
    symbol = request.form.get("symbol")

    if not shares:
        return apology("must provide shares", 403)
    if not symbol:
        return apology("must provide symbol", 403)
    if int(shares) <= 0:
        return apology("enter positive int", 403)

    transactions = db.execute("SELECT symbol, amount FROM history where userid=:id",
                              id=session["user_id"])

    maxNumberOfShares = 0
    for t in transactions:
        if t["symbol"] == symbol:
            maxNumberOfShares += t["amount"]

    if maxNumberOfShares <= 0:
        return apology("No Shares", 403)
    if maxNumberOfShares < int(shares):
        return apology("No enough Shares", 403)

    data = lookup(symbol)

    db.execute("INSERT INTO history (userid, symbol, amount, price, date) VALUES (:u, :s, :a, :p, :d)",
               u=session["user_id"],
               s=symbol,
               a=0 - int(shares),
               p=0 - data["price"],
               d=datetime.datetime.now())
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
