from functools import wraps
import tweepy
from flask import Flask, render_template, request, redirect, url_for, session, flash
import db
from CONFIG import SECRET_KEY
from make_table import get_table
from twitter_auth import authenticate
from user_management import login_db

app = Flask(__name__)

app.secret_key = SECRET_KEY


# Decorator to require log in
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "username" in session:
            return f(*args, **kwargs)
        else:
            flash("not logged in")
            return redirect(url_for("login"))
    return wrap


# Decorator to lock log in page after logged in
def no_login(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "username" not in session:
            return f(*args, **kwargs)
        else:
            flash("You are already logged in.")
            return redirect(url_for("index"))
    return wrap


# Decorator to allow only users "julian" and "admin" to certain pages
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session["username"] == ("julian" or "admin"):
            return f(*args, **kwargs)
        else:
            return render_template("no_permission.html", subheading="", page="exempt")
    return wrap


@app.route("/")
def index():
    if "logged_in" in session:
        return render_template("index.html", subheading="Home Page", page="home")
    else:
        return redirect(url_for("login"))


@app.route("/login/", methods=["GET", "POST"])
@no_login
def login():
    error = None
    if request.method == "POST":
        if login_db.verify(request.form["username"], request.form["password"]):
            session["username"] = request.form["username"]
            flash("You have been logged in!")
            return redirect(url_for("index"))
        else:
            error = "Invalid Credentials: Please try again."
    return render_template("login.html", subheading="Log In", error=error, page="exempt")


@app.route("/logout/")
@login_required
def logout():
    session.pop("username", None)
    flash("logged out")
    return redirect(url_for("login"))


@app.route("/schedule/")
@login_required
def schedule():
    return render_template("schedule.html", shows=get_table(), slots=db.read(), subheading="Schedule", page="schedule")


@app.route("/add/", methods=["GET", "POST"])
@login_required
def add_show():
    if request.method == "POST":
        show_info = [request.form["show-name"],
                     request.form["show-day"],
                     request.form["show-start"],
                     request.form["show-end"],
                     request.form["host-1"],
                     request.form["host-2"],
                     request.form["host-3"],
                     request.form["host-4"],
                     ''
                     ]
        db.add(show_info)

    return render_template("add_show.html", alert=None, subheading="Adding New Show", page="add")


@app.route("/remove/", methods=["POST"])
@login_required
def remove_show():
    show_info = request.form["slot"]
    try:
        db.remove(show_info.split("`"))
    except IndexError:
        pass
    return redirect(url_for("schedule"))


@app.route("/user-management/")
@login_required
@admin_required
def users():
    return "Hello"


@app.route("/manual-tweet/")
@login_required
def manual_tweet_page():
    return render_template("manual_tweet.html", subheading="Send Tweet Manually", status=None, page="manual-tweet")


@app.route("/manual-tweet/", methods=["POST"])
@login_required
def send_tweet():
    twit = authenticate()
    tweet = request.form["message"]
    try:
        twit.update_status(tweet)
        return render_template("manual_tweet.html", subheading="Send Tweet Manually", status="success", page="manual-tweet")
    except tweepy.error.TweepError:
        return render_template("manual_tweet.html", subheading="Send Tweet Manually", status="failed", page="manual-tweet")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", subheading=e, error=e, page="error"), 404

if __name__ == "__main__":
    app.run(debug=True)
