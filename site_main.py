from flask import Flask, render_template, request, redirect, url_for
from make_table import get_table
import db
import tweepy
from twitter_auth import authenticate


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", shows=get_table(), slots=db.read(), subheading="Schedule")


@app.route("/add/")
def add_show():
    return render_template("add_show.html", alert=None, subheading="Adding New Show")


@app.route("/add/", methods=["POST"])
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
    return render_template("add_show.html", alert=None, subheading="Adding New Show")


@app.route("/remove/", methods=["POST"])
def remove_show():
    show_info = request.form["slot"]
    try:
        db.remove(show_info.split("`"))
    except IndexError:
        pass
    return redirect(url_for("index"))


@app.route("/manual-tweet/")
def manual_tweet_page():
    return render_template("manual_tweet.html", subheading="Send Tweet Manually", status=None)


@app.route("/manual-tweet/", methods=["POST"])
def send_tweet():
    twit = authenticate()
    tweet = request.form["message"]
    try:
        twit.update_status(tweet)
        return render_template("manual_tweet.html", subheading="Send Tweet Manually", status="success")
    except tweepy.error.TweepError:
        return render_template("manual_tweet.html", subheading="Send Tweet Manually", status="failed")

# Error Handling

@app.errorhandler(404)
def page_note_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
