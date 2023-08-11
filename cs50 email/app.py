import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses arent cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def inbox():
    """Show recieved e-Mails"""
    userId = session["user_id"]
    usernameDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
    username = usernameDB[0]["username"]
    emails = db.execute("SELECT * FROM emails WHERE recipient = ?", username)
    return render_template("index.html", emails=emails)



@app.route("/compose", methods=["GET", "POST"])
@login_required
def compose():
    """Write an e-Mail"""
    if request.method == "GET":
        userId = session["user_id"]
        senderDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
        sender = senderDB[0]["username"]
        return render_template("compose.html", sender=sender)
    else:
        sender = request.form.get("sender")
        recipient = request.form.get("recipient")
        subject = request.form.get("subject")
        body = request.form.get("body")

        if not sender or not recipient or not subject or not body:
            return apology("No empty fields")

        if not re.search(r'@email\.com$', recipient):
            return apology("Invalid e-mail. Please enter an existing email.")

        db.execute("INSERT INTO emails (sender, recipient, subject, body) VALUES(?, ?, ?, ?)", sender, recipient, subject, body)

        return redirect("/sent")



@app.route("/sent")
@login_required
def sent():
    """Sent e-Mails"""
    userId = session["user_id"]
    usernameDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
    username = usernameDB[0]["username"]
    emails = db.execute("SELECT * FROM emails WHERE sender = ?", username)
    return render_template("index.html", emails=emails)

@app.route("/bin", methods=["GET", "POST"])
@login_required
def bin():
    """Move emails to the bin without deleting them"""
    if request.method == "POST":
        email_id = request.form.get("email_id")
        db.execute("UPDATE emails SET deleted = 1 WHERE id = ?", email_id)

    userId = session["user_id"]
    usernameDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
    username = usernameDB[0]["username"]

    # Retrieve the emails that are in the bin
    emails = db.execute("SELECT * FROM emails WHERE deleted = 1 AND (sender = ? OR recipient = ?)", username, username)

    return render_template("bin.html", emails=emails)


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    """Delete an e-Mail"""
    emailId = request.form.get("emailId")
    emailDetailDB = db.execute("SELECT * FROM emails WHERE id = ?", emailId)
    emailDetail = emailDetailDB[0]
    return render_template("delete_confirm.html", emailDetail=emailDetail)

@app.route("/delete-confirm", methods=["POST"])
@login_required
def delete_confirm():
    """Handle the delete confirmation"""
    emailId = request.form.get("emailId")
    confirmation = request.form.get("confirmation")

    if confirmation == "yes":
        db.execute("DELETE FROM emails WHERE id = ?", emailId)

    return redirect("/bin")


@app.route("/restore", methods=["POST"])
@login_required
def repair():
    """Restore a deleted e-Mail"""
    emailId = request.form.get("emailId")
    emailDetailDB = db.execute("SELECT * FROM emails WHERE id = ?", emailId)
    emailDetail = emailDetailDB[0]
    return render_template("restore_confirm.html", emailDetail=emailDetail)

@app.route("/restore-confirm", methods=["POST"])
@login_required
def restore_confirm():
    """Handle the restore confirmation"""
    emailId = request.form.get("emailId")
    confirmation = request.form.get("confirmation")

    if confirmation == "yes":
        db.execute("UPDATE emails SET deleted = 0 WHERE id = ?", emailId)

    return redirect("/bin")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log the user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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


@app.route("/logout")
def logout():
    """Log the user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/email", methods=["POST"])
@login_required
def e_mail():
    """e-Mail details"""
    if request.method == "POST":
        emailId = request.form.get("emailId")
        emailDetailDB = db.execute("SELECT * FROM emails WHERE id = ?", emailId)
        emailDetail = emailDetailDB[0]
        return render_template("email.html", emailDetail=emailDetail)


import re

@app.route("/register", methods=["GET", "POST"])
def sign_up():
    """Register a user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not email or not password or not confirm:
            return apology("Please enter information")

        if password != confirm:
            return apology("Passwords do not match")

        if not re.search(r'@email\.com$', email):
            return apology("Invalid email format. Please use @email.com")

        hash = generate_password_hash(password)

        try:
            newUser = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", email, hash)
        except:
            return apology("Email taken")

        session["user_id"] = newUser

        return redirect("/")


@app.route("/reply", methods=["GET", "POST"])
@login_required
def respond():
    """Reply to an e-mail"""
    if request.method == "POST":
        emailId = request.form.get("emailId")
        emailDetailDB = db.execute("SELECT * FROM emails WHERE id = ?", emailId)
        emailDetail = emailDetailDB[0]
        return render_template("reply.html", emailDetail=emailDetail)
