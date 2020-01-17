import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from help_web import apology, login_required

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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

@app.route("/")
@login_required
def index():

     # Get user's key
    session_role = session.get("key")

    # Render teacher template if user is a teacher
    if session_role == "teacher":
        return render_template("teacher_index.html")

    # Render student template if user is not a teacher
    else:
        return render_template("student_index.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    if request.method == "GET":

        # Get username and list of taken names
        username = request.args.get("username")

        # Check whether user is teacher
        if session.get("key") == "teacher":
            taken_names = db.execute("Select username FROM Teacher")
        else:
            taken_names = db.execute("Select username FROM student")

        # Check if username field is empty
        if len(str(username)) <= 0:
            return jsonify(False)

        # Check for every name in taken names if username matches one of taken names
        for taken_name in taken_names:
            if username == taken_name["username"]:
                return jsonify(False)

    # If username passes every test return true
    return jsonify(True)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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

        # Check if user is registered as a teacher
        if session.get("key") == "teacher":
            # Query database for teacher username
            rows = db.execute("SELECT * FROM Teacher WHERE username = :username",
                              username=request.form.get("username"))
        else:
            # Query database for student username
            rows = db.execute("SELECT * FROM student WHERE username = :username",
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

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password repetition was submitted
        elif not request.form.get("confirmation"):
            return apology("password repeat empty", 400)

        # Ensure password and password rep. is the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and password repeat must be the same", 400)

        password = generate_password_hash(request.form.get("password"))
        username = request.form.get("username")
        role = request.form.get("role")

        # Insert teachers into teacher database...
        if role == "teacher":
            result = db.execute("INSERT INTO Teacher(username, hash) VALUES(:username, :password)", username=username, password=password)

            # Set session key to 'teacher'
            session["key"] = "teacher"

        # ...and insert students into student database
        elif role == "student":
            result = db.execute("INSERT INTO student(username, hash) VALUES(:username, :password)", username=username, password=password)

            # Set session key to 'student'
            session["key"] = "student"

        # Ensure user selects either teacher or student
        else:
            return apology("You must choose a role", 400)

        if not result:
            return apology("username taken", 400)

        session["user_id"] = result

        return redirect("/")

    else:
        return render_template("register.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow user to change her password"""

    if request.method == "POST":

        # Ensure current password is not empty
        if not request.form.get("current_password"):
            return apology("must provide current password", 400)

        # Get password currently being used
        password = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # Ensure current password is correct
        if not check_password_hash(password[0]["hash"], request.form.get("current_password")):
            return apology("invalid password", 400)

        # Ensure new password is not empty
        if not request.form.get("new_password"):
            return apology("must provide new password", 400)

        # Ensure new password repeated is not empty
        if not request.form.get("new_password_repeat"):
            return apology("must provide new password repeat", 400)

        # Ensure new password and password repeat match
        if request.form.get("new_password") != request.form.get("new_password_repeat"):
            return apology("new password and repitition must match", 400)

        # Update database with new password
        new_password = generate_password_hash(request.form.get("new_password"))
        db.execute("UPDATE users SET hash = :new_password WHERE id = :user_id",
                    user_id=session["user_id"], new_password=new_password)

    else:
        return render_template("change_password.html")


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)