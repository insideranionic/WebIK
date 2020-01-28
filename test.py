import requests
import urllib.parse
import os

from cs50 import SQL
from flask import redirect, render_template, request, session
from functools import wraps

db = SQL("sqlite:///database.db")

quiz_id= db.execute("SELECT quiz_id FROM teach_lijst WHERE naam_quiz=:name", name="quiz1")
print(quiz_id)

