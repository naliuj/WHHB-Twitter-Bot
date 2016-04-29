import tweepy
from flask import Flask, render_template, request, redirect, url_for, session, flash
import db
from CONFIG import SECRET_KEY
from bot.twitter_auth import authenticate
from make_table import get_table
from user_management import login_db
from user_management.page_restrictions import no_login, login_required, admin_required

app = Flask(__name__)

app.secret_key = SECRET_KEY


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
            session["logged_in"] = True
            session["username"] = request.form["username"]
            flash("You have been logged in!")
            return redirect(url_for("index"))
        else:
            error = "Invalid Credentials: Please try again."
    return render_template("login.html", subheading="Log In", error=error, page="exempt")


@app.route("/logout/")
@login_required
def logout():
    session.pop("logged_in", None)
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
        return render_template("manual_tweet.html", subheading="Send Tweet Manually", status="success",
                               page="manual-tweet")
    except tweepy.error.TweepError as e:
        if session["username"] == "julian":
            return render_template("manual_tweet.html", subheading="Send Tweet Manually", status="error", error=e,
                                   page="manual-tweet")
        else:
            return render_template("manual_tweet.html", subheading="Send Tweet Manually", status="failed",
                               page="manual-tweet")


@app.route("/settings/", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        if login_db.verify(session["username"], request.form["old_pass"]):
            login_db.update(session["username"], request.form["new_pass"])
            flash("pass-updated")
        else:
            flash("bad-old")
    return render_template("settings.html", subheading="Account Settings", message=None, page="settings")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", subheading="", error=e, page="exempt"), 404

if __name__ == "__main__":
    app.run(debug=True)
