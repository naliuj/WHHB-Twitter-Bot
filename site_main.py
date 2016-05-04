import tweepy
from flask import Flask, render_template, request, redirect, url_for, session, flash
import db
from CONFIG import SECRET_KEY
from bot.twitter_auth import authenticate
from make_table import get_table
from user_management import login_db
from user_management.page_restrictions import no_login, login_required, admin_required
from user_management.table import get_table as user_table
from forms.login import LoginForm
from forms.add_show import AddShowForm
from forms.add_user import AddUserForm

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
    loginForm = LoginForm()
    if request.method == "POST" and loginForm.validate():
        if login_db.verify(loginForm.username.data, loginForm.password.data):
            session["logged_in"] = True
            session["username"] = loginForm.username.data
            session["type"] = login_db.get_type(loginForm.username.data)
            flash("You have been logged in!")
            return redirect(url_for("index"))
        else:
            error = "Invalid Credentials: Please try again."
    return render_template("login.html", subheading="Log In", error=error, loginForm=loginForm, page="exempt")


@app.route("/logout/")
@login_required
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    session.pop("type", None)
    flash("logged out")
    return redirect(url_for("login"))


@app.route("/schedule/")
@login_required
def schedule():
    return render_template("schedule.html", shows=get_table(), slots=db.read(), subheading="Schedule", page="schedule")


@app.route("/add/", methods=["GET", "POST"])
@login_required
def add_show():
    showForm = AddShowForm()
    if request.method == "POST" and showForm.validate():
        show_info = [showForm.showName.data,
                     showForm.showDay.data,
                     showForm.showStart.data,
                     showForm.showEnd.data,
                     showForm.host1.data,
                     showForm.host2.data,
                     showForm.host3.data,
                     showForm.host4.data,
                     ''
                     ]
        db.add(show_info)
        return redirect(url_for("add_show"))

    return render_template("add_show.html", alert=None, showForm=showForm, subheading="Adding New Show", page="add")


@app.route("/remove/<day>/<start>/<end>/")
@login_required
def remove_show(day, start, end):
    try:
        db.remove([day, start, end])
    except IndexError:
        pass
    return redirect(url_for("schedule"))


@app.route("/user-management/", methods=["GET", "POST"])
@login_required
@admin_required
def users():
    addUser = AddUserForm()
    if request.method == "POST" and addUser.validate():
        login_db.add([addUser.username.data, addUser.password.data, addUser.type.data])
        return redirect(url_for("users"))
    return render_template("user_management.html", subheading="User Management", addUser=addUser, table=user_table(),
                           accounts=login_db.read(), page="user-management")


@app.route("/user-management/user/<username>/")
@login_required
@admin_required
def user_profile(username):
    for row in login_db.read():
        if row[0] == username:
            return render_template("user_profile.html", subheading="Viewing {}".format(username), username=username,
                                   type=row[2], user_exists=True, page="user-profile")
    else:
        return render_template("user_profile.html", subheading="Not Found", username=username, type=None,
                               user_exists=False, page="user-profile")


@app.route("/user-management/user/delete/<username>/")
@login_required
@admin_required
def delete_user(username):
    login_db.remove(username)
    return redirect(url_for("users"))


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
        if session["type"] == "dev":
            return render_template("manual_tweet.html", subheading="Send Tweet Manually", status="error", error=e,
                                   page="manual-tweet")
        else:
            return render_template("manual_tweet.html", subheading="Send Tweet Manually", status="failed",
                                   page="manual-tweet")


@app.route("/settings/", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        if login_db.verify(session["username"], request.form["old_pass"]):
            login_db.update(session["username"], request.form["new_pass"])
            flash("pass-updated")
        else:
            flash("bad-old")
    return render_template("change_pass.html", subheading="Account Settings", message=None, page="settings")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", subheading="", error=e, page="exempt"), 404

if __name__ == "__main__":
    app.run(debug=True)
