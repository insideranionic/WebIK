import os

import json
import random
import requests
import urllib.request
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from help_web import apology, convert, convert_question, login_required, to_csv

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


@app.route("/homepage", methods=["GET", "POST"])
def homepage():
    return render_template("homepage.html")

@app.route("/homepage_2", methods=["GET", "POST"])
@login_required
def homepage_2():
    return redirect("/")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

     # Get user's key
    session_role = session.get("key")

    # Render teacher template if user is a teacher
    if session_role == "teacher":

        if request.method == "POST":

            # Get name of quiz
            name = request.form.get("name")

            # Get desired amount of questions for new quiz
            aantal_vragen = request.form.get("questions")

            # Get desired difficulty
            difficulty = request.form.get("difficulty")

            # Get desired category
            category = request.form.get("category")

            # Get type of quiz (default = multiple choice)
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


            # Add data to database
            # db.execute("INSERT INTO new_quizes(amount_of_questions, difficulty, category, type, name, username_teacher) VALUES (:amount, :difficulty, :category, :type_q, :name, :username_teacher)",
            #             amount=amount, difficulty=difficulty, category=category, type_q=type_q, name=name, username_teacher=username_teacher)


            return redirect("/")
        else:
            categorie= ["History","Politics", "Geography"]
            return render_template("teacher_index.html", categorie= categorie)

    # Render student template if user is not a teacher
    else:
        return render_template("student_index.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    if request.method == "GET":

        # Get username and list of taken names
        username = request.args.get("username")
        taken_names_teach = db.execute("Select username FROM Teachers")
        taken_names = taken_names_teach + db.execute("Select username FROM student")

        # Check if username field is empty
        if len(str(username)) <= 0:
            return jsonify(False)

        # check for every name in taken names if username matches one of taken names
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
            return render_template("login.html", error_message="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", error_message="must provide password")


        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password",)

        # Check if user is registered as a teacher
        role = request.form.get("role")

        if role == "teacher":
            # Query database for teacher username
            rows = db.execute("SELECT * FROM Teacher WHERE username = :username",
                              username=request.form.get("username"))

            session["key"] = "teacher"

        else:
            # Query database for student username
            rows = db.execute("SELECT * FROM student WHERE username = :username",
                              username=request.form.get("username"))
            session["key"] = "student"

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", error_message="invalid username and/or password")


        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user"] = request.form.get("username")

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
            return render_template("register.html", error_message="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("register.html", error_message="must provide password")

        # Ensure password repetition was submitted
        elif not request.form.get("confirmation"):
            return render_template("register.html", error_message="password repeat empty")

        # Ensure password and password rep. is the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html", error_message="password and password repeat must be the same")

        password = generate_password_hash(request.form.get("password"))
        username = request.form.get("username")
        role = request.form.get("role")

        # Insert teachers into teacher database...
        if role == "teacher":
            username_check =  db.execute("SELECT * FROM teacher WHERE username = :username", username=username)
            if  username_check:
                return render_template("register.html", error_message = "username is taken")
            result = db.execute("INSERT INTO Teacher(username, hash) VALUES(:username, :password)", username=username, password=password)

            # Set session key to 'teacher'
            session["key"] = "teacher"

        # ...and insert students into student database
        elif role == "student":
            username_check =  db.execute("SELECT * FROM student WHERE username = :username", username=username)
            if  username_check:
                return render_template("register.html", error_message = "username is taken")
            result = db.execute("INSERT INTO student(username, hash) VALUES(:username, :password)", username=username, password=password)

            # Set session key to 'student'
            session["key"] = "student"

        # Ensure user selects either teacher or student
        else:
            return render_template("register.html", error_message="You must choose a role")

        if not result:
            return render_template("register.html", error_message="username taken")

        session["user_id"] = result

        return redirect("/login")

    else:
        return render_template("register.html")

# return results of student
@app.route("/result", methods=["GET", "POST"])
def result():
    session_role = session.get("key")
    if session_role == "student":
        result_sql = db.execute("SELECT username, result, quiz_name, category, date FROM student_results where id = :user_id", user_id=session["user_id"])
        return render_template("result.html", result_sql=result_sql)
    else:
        result_sql = db.execute("SELECT username, result, quiz_name, category, date FROM student_results where teacher_name = :user_id", user_id=session["user"])
        return render_template("result.html", result_sql=result_sql)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow user to change her password"""

    if request.method == "POST":

        # Ensure current password is not empty
        if not request.form.get("current_password"):

            return render_template("change_password.html", error_message="must provide current password")

        sess_role = session.get("key")
        if sess_role == 'teacher':
            # Get password currently being used
            password = db.execute("SELECT hash FROM Teacher WHERE id = :user_id", user_id=session["user_id"])
        else:
            # Get password currently being used
            password = db.execute("SELECT hash FROM student WHERE id = :user_id", user_id=session["user_id"])

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

        # Update database with new password
        new_password = generate_password_hash(request.form.get("new_password"))
        db.execute("UPDATE users SET hash = :new_password WHERE id = :user_id",
                    user_id=session["user_id"], new_password=new_password)

    else:
        return render_template("change_password.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    quiz_id= session["quiz_id"]
    quiz_id= quiz_id[0]["quiz_id"] #functie3
    quiz_data= db.execute("SELECT * FROM teach_lijst WHERE quiz_id= :id", id = quiz_id)[0]
    quiz_answers = quiz_data['all_answer_sheets']
    quiz_questions = quiz_data["vragen_lijst"]



    #  make the quiz answers into a csv type output and convert it into a list


    # quiz_answers = quiz_answers.replace("[",""); #functie2
    # quiz_answers = quiz_answers.replace("]","");
    # quiz_answers = quiz_answers.replace("'","");
    # quiz_answers = quiz_answers.replace(" ",""); #functie2

    to_csv(quiz_answers)
    quiz_answer_list = convert(quiz_answers)

    # make the questions into a csv type output and convert it into a list
    question_list = convert_question(quiz_questions)



    single_ans_sheet = []
    all_answer_sheets = []
    correct_answers = []
    question_value_dict = {}
    question_answer_dict = {}
    counter = 0


    # make a list with list(these contain the choices of the question)
    for answer in quiz_answer_list:
        counter += 1
        single_ans_sheet.append(answer)
        if counter % 4 == 0:
            all_answer_sheets.append(single_ans_sheet)
            single_ans_sheet = []


    # make a list of correct answers ( 3 is the location of the right answers in the list)
    for answers in all_answer_sheets:
        correct_answers.append(answers[3])

    question_index = 0
    for question in question_list:
        question_value_dict[question] = question_index
        question_index += 1


    for questions in question_list:
        question_answer_dict[questions] = correct_answers[0]

    if request.method == "GET":
        session["result"] = 0
        answer_list = all_answer_sheets[0]
        question = question_list[0]
        return render_template("quiz.html", question = question , answers = answer_list)
    else:
        answer = request.form.get("answer")
        question = request.form.get("question_hidden")
        # -1 to retrieve index of next question
        new_question = int(question_value_dict[question]) + 1

        if new_question == len(question_value_dict) - 1:

            info = db.execute("SELECT naam_teach, naam_quiz, category FROM teach_lijst WHERE quiz_id=:quiz_id", quiz_id = quiz_id) #functie1
            teacher_name= info[0]["naam_teach"]
            quiz_name= info[0]["naam_quiz"]
            category= info[0]["category"]

            # quiz_name = db.execute("SELECT naam_quiz FROM teach_lijst WHERE quiz_id=:quiz_id", quiz_id = quiz_id) #functie1
            # quiz_name= quiz_name[0]["naam_quiz"]

            # category = db.execute("SELECT category FROM teach_lijst WHERE quiz_id=:quiz_id", quiz_id = quiz_id) #functie1
            # category= category[0]["category"]

            db.execute("INSERT INTO student_results(id, username, result, teacher_name, quiz_name, category, quiz_id) VALUES(:user_id, :username, :result, :teacher_name, :quiz_name, :category, :quiz_id)"
                        ,user_id=session["user_id"], username=session["user"], result=session["result"], teacher_name=teacher_name, quiz_name=quiz_name, category=category, quiz_id=quiz_id )

            db.execute("INSERT INTO leaderboard(username, result, quiz_name, quiz_id) VALUES(:username, :result, :quiz_name, :quiz_id)"
                        ,username=session["user"], result=session["result"], quiz_name=quiz_name, quiz_id=quiz_id)

            leader= db.execute("SELECT * FROM leaderboard WHERE quiz_id = :quiz_id ORDER BY [result] DESC LIMIT 3", quiz_id=quiz_id)
            return render_template("leaderboard.html", leader = leader)

        else:
            question = question_list[new_question]
            answer_list =  all_answer_sheets[new_question]
            answer_list = random.sample(answer_list, len(answer_list))

            if answer in correct_answers:
                session["result"] += 1

            return render_template("quiz.html", question = question , answers = answer_list)


@app.route("/leaderboard")
def leaderboard():
    """Shows user leaderboard"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("leaderboard.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    """search for room"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        name = request.form.get("search")
        quizes = db.execute("SELECT naam_quiz FROM teach_lijst")
        if name not in quizes:
            return render_template("search.html", error_message="quiz doesn't exist, try again")

        quiz_id= db.execute("SELECT quiz_id FROM teach_lijst WHERE naam_quiz=:name", name=name)
        session["quiz_id"] = quiz_id
        return redirect(url_for("quiz"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("search.html")


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


@app.route("/FAQ", methods=["GET", "POST"])
def faq():
    return render_template("FAQ.html")
