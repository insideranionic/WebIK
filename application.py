import os

import random
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
        taken_names_teach = db.execute("Select username FROM Teachers")
        taken_names_student = db.execute("Select username FROM student")

        # Check if username field is empty
        if len(str(username)) <= 0:
            return jsonify(False)

        # check for every name in taken names if username matches one of taken names
        for taken_name in taken_names_teach:
            if username == taken_name["username"]:
                return jsonify(False)

        for taken_name in taken_names_student:
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

# return results of student
@app.route("/leader", methods=["GET", "POST"])
def result():
    result_sql = db.execute("SELECT username, result, room_name, quiz_name, category, date FROM student_results where student_id = 1" )
    print(result)

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

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    quiz = {"response_code":0,"results":[{"category":"Geography","type":"multiple","difficulty":"hard","question":"What is the largest city and commercial capital of Sri Lanka?","correct_answer":"Colombo","incorrect_answers":["Moratuwa","Negombo","Kandy"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"Which of these countries is NOT a part of the Asian continent?","correct_answer":"Suriname","incorrect_answers":["Georgia","Russia","Singapore"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"Which country is completely landlocked by South Africa?","correct_answer":"Lesotho","incorrect_answers":["Swaziland","Botswana","Zimbabwe"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"Which of these is NOT a province in China?","correct_answer":"Yangtze","incorrect_answers":["Fujian","Sichuan","Guangdong"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"The mountainous Khyber Pass connects which of the two following countries?","correct_answer":"Afghanistan and Pakistan","incorrect_answers":["India and Nepal","Pakistan and India","Tajikistan and Kyrgyzstan"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"What is the name of one of the Neo-Aramaic languages spoken by the Jewish population from Northwestern Iraq?","correct_answer":"Lishana Deni","incorrect_answers":["Hulaul&aacute;","Lishan Didan","Chaldean Neo-Aramaic"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"Which of the following Inuit languages was the FIRST to use a unique writing system not based on the Latin alphabet?","correct_answer":"Inuktitut","incorrect_answers":["Inuinnaqtun","Greenlandic","Inupiat"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"Where is the Luxor Hotel &amp; Casino located?","correct_answer":"Paradise, Nevada","incorrect_answers":["Las Vegas, Nevada","Winchester, Nevada","Jackpot, Nevada"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"What year is on the flag of the US state Wisconsin?","correct_answer":"1848","incorrect_answers":["1634","1783","1901"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"How many countries border Kyrgyzstan?","correct_answer":"4","incorrect_answers":["3","1","6"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"Llanfair&shy;pwllgwyngyll&shy;gogery&shy;chwyrn&shy;drobwll&shy;llan&shy;tysilio&shy;gogo&shy;goch is located on which Welsh island?","correct_answer":"Anglesey","incorrect_answers":["Barry","Bardsey","Caldey"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"The Hunua Ranges is located in...","correct_answer":"New Zealand","incorrect_answers":["Nepal","China","Mexico"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"Fucking is a village in which country?","correct_answer":"Austria","incorrect_answers":["Germany","Switzerland","Czech Republic"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"What is the name of the Canadian national anthem?","correct_answer":"O Canada","incorrect_answers":["O Red Maple","Leaf-Spangled Banner","March of the Puck Drop"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"What North American tourist attraction is served by the &quot;Maid of the Mist&quot; tour company?","correct_answer":"Niagara Falls","incorrect_answers":["Whistler, British Columbia","Disney World","Yosemite National Park"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"What is the name of rocky region that spans most of eastern Canada?","correct_answer":"Canadian Shield","incorrect_answers":["Rocky Mountains","Appalachian Mountains","Himalayas"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"What is Canada&#039;s largest island?","correct_answer":"Baffin Island","incorrect_answers":["Prince Edward Island","Vancouver Island","Newfoundland"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"What is the name of the formerly rich fishing grounds off the island of Newfoundland, Canada?","correct_answer":"Grand Banks","incorrect_answers":["Great Barrier Reef","Mariana Trench","Hudson Bay"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"When does Finland celebrate their independence day?","correct_answer":"December 6th","incorrect_answers":["January 2nd","November 12th","February 8th"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"What is the land connecting North America and South America?","correct_answer":"Isthmus of Panama","incorrect_answers":["Isthmus of Suez","Urals","Australasia"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"Which of these cities has a 4&deg; East longitude. ","correct_answer":"Amsterdam","incorrect_answers":["Rio de Janero","Toronto","Hong Kong"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"The Andaman and Nicobar Islands in South East Asia are controlled by which country?","correct_answer":"India","incorrect_answers":["Vietnam","Thailand","Indonesia"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"What is the capital of Mauritius?","correct_answer":"Port Louis","incorrect_answers":["Port Moresby","Port Vila","Port-au-Prince"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"In which country is Tallinn located?","correct_answer":"Estonia","incorrect_answers":["Finland","Sweden","Poland"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"Into which basin does the Jordan River flow into?","correct_answer":"Dead Sea","incorrect_answers":["Aral Sea","Caspian Sea","Salton Sea"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"The emblem on the flag of the Republic of Tajikistan features a sunrise over mountains below what symbol?","correct_answer":"Crown","incorrect_answers":["Bird","Sickle","Tree"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"The Maluku islands (informally known as the Spice Islands) belong to which country?","correct_answer":"Indonesia","incorrect_answers":["Chile","New Zealand","Fiji"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"What national museum will you find in Cooperstown, New York?","correct_answer":"National Baseball Hall of Fame","incorrect_answers":["Metropolitan Museum of Art","National Toy Hall of Fame","Museum of Modern Art"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"Which of these cities is NOT in England?","correct_answer":"Edinburgh","incorrect_answers":["Oxford","Manchester","Southampton"]},{"category":"Geography","type":"multiple","difficulty":"hard","question":"Which country is the Taedong River in?","correct_answer":"North Korea","incorrect_answers":["South Korea","Japan","China"]}]}

    all_questions  = (quiz['results'])
    question_ans_dict = {}
    all_answers = []

    for x in range(len(all_questions)):
        possible_answers = []
        possible_answers.clear()
        question_single = (all_questions[x])
        incorrect_answers = question_single['incorrect_answers']
        print(question_single['question'])

        for incorrect in incorrect_answers:
            possible_answers.append(incorrect)

        possible_answers.append(question_single['correct_answer'])
        all_answers.append(question_single['correct_answer'])
        question_ans_dict[str(question_single['question'])] = possible_answers

    # key list makes it possible to get to questions via numbers
    # so if a user wants to got to tanother question we can  add +1 or -1 to the current position
    key_list = list(question_ans_dict.keys())

    for x in range(len(key_list)):
        question = key_list[x]
        answer_list = question_ans_dict[str(question)]
        answer_1 = random.choice(answer_list)

        #  check if every answer in the multiple choice display is unique
        answer_2 = random.choice(answer_list)
        if answer_2 == answer_1:
            answer_2 = random.choice(answer_list)
            while answer_2 == answer_1:
                answer_2 = random.choice(answer_list)

        answer_3 = random.choice(answer_list)
        if answer_3 == answer_1 or answer_3 == answer_2:
            answer_3 = random.choice(answer_list)
            while answer_3 == answer_1 or answer_3 == answer_2:
                answer_3 = random.choice(answer_list)

        answer_4 = random.choice(answer_list)
        if answer_4 == answer_1 or answer_4== answer_2 or answer_4 == answer_3:
            answer_4 = random.choice(answer_list)
            while answer_4 == answer_1 or answer_4== answer_2 or answer_4 == answer_3:
                answer_4 = random.choice(answer_list)


@app.route("/leaderboard", methods=["GET", "POST"])
def leaderboard():
    """shows user his scores"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("leaderboard.html")


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
