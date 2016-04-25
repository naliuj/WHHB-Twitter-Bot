from flask import Flask, render_template, request, redirect, url_for
from make_table import get_table
import db


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", shows=get_table())


@app.route("/add/")
def add_show():
    return render_template("add_show.html", alert=None)


@app.route("/added/", methods=["POST"])
def added_show():
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
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
