from flask import Blueprint, render_template,redirect, session,url_for, flash,g
from mydb import getposts, getmyposts
import os,mimetypes,base64

views = Blueprint("views",__name__)

@views.before_request
def make_session_permanent():
    session.permanent = True  # Make the session use the PERMANENT_SESSION_LIFETIME
    session.modified = True  # Refresh session timeout with each request
    if 'user_id' in session:
        g.user_id = session['user_id']
    else:
        g.user_id = None  # Ensure g.user_id is None if the session has expired or the user is not logged in


@views.route("/homepage")
def homepage():
    return render_template("homepage.html")

@views.route("/posts")
def posts():
    if 'user_id' in session:
        postslist = getposts()
        userposts = getmyposts(g.user_id)
        if userposts:
            return render_template('posts.html', posts = postslist, base64 = base64, mimetypes = mimetypes )
        flash("you have to tell a secret to see a secret ;)")
        return render_template("posts.html")
    flash("you're not logged in.")
    return redirect(url_for("views.homepage"))

@views.route("/posts/myposts")
def myposts():
    if 'user_id' in session:
        user_id = g.user_id
        myposts = getmyposts(user_id)
        return render_template("posts.html", posts = myposts, base64 = base64, os = os )
    flash("you're not logged in.")
    return redirect(url_for("views.homepage"))
