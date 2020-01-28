import requests
import urllib.parse
import os

from cs50 import SQL
from flask import redirect, render_template, request, session
from functools import wraps
from werkzeug.security import check_password_hash

db = SQL("sqlite:///database.db")

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/homepage")
        return f(*args, **kwargs)
    return decorated_function

def apology(message):

    return message

def convert(string):
    li = list(string.split(","))
    return li

def convert_question(string):
    li = list(string.split("?"))
    return li

def to_csv(i):
    i = i.replace("[","");
    i = i.replace("]","");
    i = i.replace("'","");
    i = i.replace(" ","");
    return i

def quiz_list():
    select = db.execute("SELECT naam_quiz FROM teach_lijst")
    naam = []
    for name in select:
        name = name["naam_quiz"]
        naam.append(name)
    return naam

def quiz_id(name):
    quiz_id= db.execute("SELECT quiz_id FROM teach_lijst WHERE naam_quiz=:name", name=name)
    return quiz_id

def leaderbord(quiz_id):
    leader= db.execute("SELECT * FROM leaderboard WHERE quiz_id = :quiz_id ORDER BY [result] DESC LIMIT 3", quiz_id=quiz_id)
    return leader

def leaderbord_insert(i,j,k,l):
     db.execute("INSERT INTO leaderboard(username, result, quiz_name, quiz_id) VALUES(:username, :result, :quiz_name, :quiz_id)",username=i, result=j, quiz_name=k, quiz_id=l)
     return

def student_result_insert(i,j,k,l,m,n,o):
    db.execute("INSERT INTO student_results(id, username, result, teacher_name, quiz_name, category, quiz_id) VALUES(:user_id, :username, :result, :teacher_name, :quiz_name, :category, :quiz_id)"
                ,user_id=i, username=j, result=k, teacher_name=l, quiz_name=m, category=n, quiz_id=o)
    return

def info_teach(quiz_id):
    info = db.execute("SELECT naam_teach, naam_quiz, category FROM teach_lijst WHERE quiz_id=:quiz_id", quiz_id = quiz_id) #functie1

    try:
        return {
            "name": info[0]["naam_teach"],
            "quiz_naam": info[0]["naam_quiz"],
            "category": info[0]["category"]
        }
    except (KeyError, TypeError, ValueError):
        return None

def check_changepass(password):

    # Ensure current password is correct
    if not check_password_hash(password[0]["hash"], request.form.get("current_password")):
        return render_template("change_password.html", error_message="invalid password")

    # Ensure new password is not empty
    if not request.form.get("new_password"):
        return render_template("change_password.html", error_message="must provide new password")

    # Ensure new password repeated is not empty
    if not request.form.get("new_password_repeat"):
        return render_template("change_password.html", error_message="must provide new password repeat")

    # Ensure new password and password repeat match
    if request.form.get("new_password") != request.form.get("new_password_repeat"):
        return render_template("change_password.html", error_message="new password and repitition must match")

    # Ensure new password is not empty
    if not request.form.get("new_password"):
        return apology("must provide new password")

    return True

def password_t(id_num):
    return db.execute("SELECT hash FROM Teacher WHERE id = :user_id", user_id=id_num)

def password_s(id_num):
    return db.execute("SELECT hash FROM student WHERE id = :user_id", user_id=id_num)