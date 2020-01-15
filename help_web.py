import requests
import urllib.parse
import os

from flask import redirect, render_template, request, session
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup():

    # Contact API
    try:
        main_api= “https://opentdb.com/api.php?”
        url= main_api + urlib.parse.urlencode({‘amount’: aantal_vragen}) + “&” + urlib.parse.urlencode({‘category’: categorie}) + “&” +  urlib.parse.urlencode({‘difficulty’: diff} + “&” + urlib.parse.urlencode({‘type’: type}
        api_data= request.get(url)[“results”]
        api_data.raise_for_status()

    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = api_data.json()
        return {
            "amount_questions": quote["amount"],
            "category": (quote["category"]),
            "diff": quote["difficulty"]
        }
    except (KeyError, TypeError, ValueError):
        return None

