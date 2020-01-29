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
    i = convert(i)
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
        return False

    # Ensure new password is not empty
    if not request.form.get("new_password"):
        return False

    # Ensure new password repeated is not empty
    if not request.form.get("new_password_repeat"):
        return False

    # Ensure new password and password repeat match
    if request.form.get("new_password") != request.form.get("new_password_repeat"):
        return False

    # Ensure new password is not empty
    if not request.form.get("new_password"):
        return False

    return True

def check_register():

    # Ensure username was submitted
    if not request.form.get("username"):
        return False

    # Ensure password was submitted
    elif not request.form.get("password"):
        return False

    # Ensure password repetition was submitted
    elif not request.form.get("confirmation"):
        return False

    # Ensure password and password rep. is the same
    elif request.form.get("password") != request.form.get("confirmation"):
        return False

    return True

def password_t(id_num):
    return db.execute("SELECT hash FROM Teacher WHERE id = :user_id", user_id=id_num)

def password_s(id_num):
    return db.execute("SELECT hash FROM student WHERE id = :user_id", user_id=id_num)

def res():
    session_role = session.get("key")
    if session_role == "student":
        result_sql = db.execute("SELECT username, result, quiz_name, category, date FROM student_results where id = :user_id", user_id=session["user_id"])
        return result_sql
    else:
        result_sql = db.execute("SELECT username, result, quiz_name, category, date FROM student_results where teacher_name = :user_id", user_id=session["user"])
        return result_sql

def check_login():

    # Ensure username was submitted
    if not request.form.get("username"):
        return False

    # Ensure password was submitted
    elif not request.form.get("password"):
        return False

    # Ensure password was submitted
    elif not request.form.get("password"):
        return False

    # ensure user submitted role
    elif not request.form.get("role"):
        return False

    return True

def create_quiz():

    # Get desired information
    name = request.form.get("name")
    aantal_vragen = request.form.get("questions")
    difficulty = request.form.get("difficulty")
    category = request.form.get("category")
    type_q = request.form.get("type")
    username_teacher = request.form.get("username")

    category_dict= {"History": 23, "Politics": 24, "Geography": 22}
    difficulty_dict= {"easy": "easy", "medium": "medium", "hard": "hard"}
    cat= category_dict[category]
    diff= difficulty_dict[difficulty]

    # dit fixt wat je boven bij quiz wou
    main_api= "https://opentdb.com/api.php?"
    url= main_api + urllib.parse.urlencode({'amount': aantal_vragen}) + "&" + urllib.parse.urlencode({'category': cat}) + "&" +  urllib.parse.urlencode({'difficulty': diff}) + "&" + urllib.parse.urlencode({'type': type_q})
    quiz = requests.get(url).json()
    all_questions  = (quiz['results'])

    question_list = []
    correct_answers = []
    all_answer_sheets = []
    x = 0

    for x in range(len(all_questions)):
        answer_question = []
        answer_question = all_questions[x]['incorrect_answers']
        answer_question.append(all_questions[x]['correct_answer'])
        correct_answers.append(all_questions[x]['correct_answer'])
        all_answer_sheets.append(answer_question)
        question_list.append(all_questions[x]['question'])

    all_answer_sheets = str(all_answer_sheets)
    db.execute("INSERT INTO teach_lijst(naam_teach, naam_quiz, category, vragen_lijst, correct_answers, all_answer_sheets) VALUES(:username_teacher, :name, :category, :quiz, :correct_answers, :all_answer_sheets)",
                username_teacher=username_teacher, name=name, category=category, quiz=question_list, correct_answers=correct_answers, all_answer_sheets=all_answer_sheets)
    return

def teach_select(quiz_id):
    quiz_data= db.execute("SELECT * FROM teach_lijst WHERE quiz_id= :id", id = quiz_id)[0]
    return quiz_data

def update_t(passw):
    db.execute("UPDATE Teacher SET hash = :new_password WHERE id = :user_id",
                        user_id=session["user_id"], new_password=passw)
    return


def update_s(passw):
    db.execute("UPDATE student SET hash = :new_password WHERE id = :user_id",
            user_id=session["user_id"], new_password=passw)
    return

def selec_t():
    rows = db.execute("SELECT * FROM Teacher WHERE username = :username",
                  username=request.form.get("username"))
    return rows

def selec_s():
    rows = db.execute("SELECT * FROM student WHERE username = :username",
                      username=request.form.get("username"))
    return rows