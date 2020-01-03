import os
import sqlite3
import spotipy

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from datetime import datetime


from helpers import apology, login_required, lookup, usd, is_number
from spotipyAnalyzer import *

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
# db = SQL("sqlite:///finance.db")


@app.route("/")
# @login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")

        # Ensure username was submitted
        if not username:
            flash("Must provide username!")
            return render_template("login.html")

        # Check if username is valid
        setUser(username)

        session["user_id"] = username

        # Redirect user to home page
        flash("Welcome!")
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


@app.route("/playlists")
def playlists():
    """begining pages"""
    results = get_playlists()
    # print(results)
    rows = []
    for item in results["items"]:
        row = {}
        row["name"] = item["name"]
        row["text"] = item["description"]
        if item["images"]:
            row["imgUrl"] = item["images"][0]["url"]
        else:
            row["imgUrl"] = "https://developer.spotify.com/assets/branding-guidelines/icon3@2x.png"
        row["id"] = item["id"]
        rows.append(row)
    return render_template("playlists.html", rows=rows, size=len(rows))


@app.route("/playlist_stats/<i>")
def playlist_stats(i):
    if not i:
        return redirect("/")
    i = int(i)

    #track ids
    sid = []

    #get info about playlist
    results = get_playlists()
    info = {}
    row = results["items"][i]
    info["name"] = row["name"]
    info["text"] = row["description"]
    if row["images"]:
        info["imgUrl"] = row["images"][0]["url"]
    else:
        info["imgUrl"] = "https://developer.spotify.com/assets/branding-guidelines/icon3@2x.png"
    pid = row["id"]
    

    #get tracks on playlistS
    results = get_playlist(pid)
    rows = filterInfoFromPlaylist(results)

    #get audio features
    for row in rows:
        sid.append(row["id"])
    features = avgAudioFeatures(sid)
    print(features)

    return render_template("playlist_stats.html", rows=rows, info=info, features=features,)


@app.route("/songs", methods=["GET", "POST"])
def songs():
    if request.method == "POST":
        title = request.form.get("search")
        # search titles
        if not title:
            flash("Must provide title!")
            return render_template("songs.html")

        results = search_track(title)
        rows = filterInfoFromSearch(results)
        
        return render_template("songs.html", rows=rows)
    else:
        return render_template("songs.html")


@app.route("/song/<sid>")
def song(sid):
    if not sid:
        return redirect("/")
    print(sid)
    info = filterInfoFromTrack(sid)
    
    #features = get_audio_features(sid)
    features = avgAudioFeatures(sid)
    return render_template("song.html", info=info, features=features)


# link to html
# https://stackoverflow.com/questions/27539309/how-do-i-create-a-link-to-another-html-page

# def errorhandler(e):
#    """Handle error"""
#    if not isinstance(e, HTTPException):
#        e = InternalServerError()
#    return apology(e.name, e.code)


# Listen for errors
# for code in default_exceptions:
#     app.errorhandler(code)(errorhandler)
