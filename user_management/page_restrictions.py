from functools import wraps
from flask import redirect, session, url_for, flash, render_template


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