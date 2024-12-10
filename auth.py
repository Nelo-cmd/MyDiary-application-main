from flask import Blueprint, render_template,redirect, request,flash,session,g,url_for
from forms import Signupform, Loginform, Postform, logoutform,deletepostform
from mydb import getpassword,adduser, getusernamecolumn, getEmailcolumn, getuser_id, addentry, getpostuserid,deleteuserpost, get_post_id_post
from datetime import datetime
import os,base64

#define auth blueprint
auth = Blueprint("auth",__name__)


@auth.before_request
def make_session_permanent():
    session.permanent = True  # Make the session use the PERMANENT_SESSION_LIFETIME
    session.modified = True  # Refresh session timeout with each request
    if 'user_id' in session:
        g.user_id = session['user_id']
    else:
        g.user_id = None  # Ensure g.user_id is None if the session has expired or the user is not logged in


#signup route
@auth.route("/signup", methods = ['GET', "POST"])
def sign_up():
    form = Signupform()
    if request.method == "POST" and form.validate_on_submit():
        #collect data from form
        Username= request.form.get("username")
        Password = form.password.data
        Email = form.Email.data
        #collect username and email data from db
        usernamecheck = getusernamecolumn(Username)
        Emailcheck = getEmailcolumn(Email)
        #check if user aleady as an account
        if  not usernamecheck and not Emailcheck:
            adduser(Username,Email,Password)
            flash("You're signed up!", category="success")
            return redirect(url_for("views.homepage"))
        elif usernamecheck and not Emailcheck:
            flash("This username already exists", category = "error")
        else:
            print(not usernamecheck)
            print(not Emailcheck)
            flash("You already have an account. Try logging in.")
            return redirect(url_for("views.homepage"))
    return render_template("signup.html", form = form)
        

#login route
@auth.route("/loginusername", methods = ['GET', "POST"])
def login_with_username():
    form = Loginform() #define login form
    
    if request.method == "POST" and form.validate_on_submit():
        csrf_token = session.get('_csrf_token')
        print("CSRF Token (Backend):", csrf_token)

        print("home post")
        try:
            session.pop("user_id")#remove any user id in session
        except KeyError:
            pass
        Username= form.username.data#get data from form
        Email = form.Email.data
        Password = form.password.data
        checkusername= getusernamecolumn(Username) # check if username exists in database
        if checkusername:
            dbpassword = getpassword(Username=Username, Email=Email) #get password from db
            if Password == dbpassword: # check password
                session['user_id'] = getuser_id(Username,Email) #add userid to session
                return redirect(url_for("views.posts"))
            flash("wrong password")
            return redirect(url_for("auth.login_with_username"))
        flash("You don't have an account. Sign up.")
        return redirect(url_for("auth.sign_up"))
    return render_template("loginusername.html", form = form)

#login route
@auth.route("/Loginemail", methods = ['GET', "POST"])
def login_with_email():
    form = Loginform()
    if request.method == "POST" and form.validate_on_submit():
        try:
            session.pop("user_id")
        except KeyError:
            pass
        Username= form.username.data
        Email = form.Email.data
        Password = form.password.data
        checkemail = getEmailcolumn(Email)
        if checkemail:
            dbpassword = getpassword(Username=Username, Email=Email)
            if Password == dbpassword:
                session['user_id'] = getuser_id(Username,Email)
                return redirect(url_for("views.posts"))
            flash("wrong password", category= "error")
            return redirect(url_for("auth.login_with_email"))
        flash("You don't have an account. Sign up.", category= "error")
        return redirect(url_for("auth.sign_up"))
    return render_template("loginemail.html", form = form)

@auth.route("/newpost", methods = ['GET', "POST"])
def newpost():
    if 'user_id' in session:
        form = Postform()
        if request.method == "POST" and form.validate_on_submit():
            Newentry = request.form.get("Entry")
            user_id = g.user_id
            media = request.files["File"]
            file_extension = os.path.splitext(media.filename)[1].lower()[1:]
            file_data = media.read() if media else None
            time = datetime.now()
            addentry(Newentry, user_id, file_extension, file_data, time)
            flash("You have another secret!", category= "success")
            return redirect(url_for("views.posts"))
        return render_template("newpost.html", form = form)
    flash("you're not logged in.")
    return redirect(url_for("views.homepage"))


@auth.route("/posts/confirmdelete", methods = ["GET","POST"])
def confirm_delete():
    form = deletepostform()
    
    if 'user_id' in session:
        
        if request.method == "POST" and form.validate_on_submit():
            post_id = request.form.get("post_id")
            deletepost = request.form.get("deletepost")
            user_id = g.user_id  # Assuming `g.user` contains the logged-in user's ID
            dbuser_id = getpostuserid(post_id)  # Get the post's user ID from the database
            if deletepost:
                if user_id == dbuser_id[0]:  # Check if the current user owns the post
                    deleteuserpost(post_id)  # Delete the post
                    flash("Post deleted ;)", category="success")
                    return redirect(url_for("views.posts"))  # Redirect after deletion

                flash("You can't delete a post that isn't yours.", "error")
                return redirect(url_for("views.posts"))  # Redirect if deletion isn't allowed
            
            return redirect(url_for("views.posts"))
    
        post_id = request.args.get("post_id")  # Get post_id from query string
        post = get_post_id_post(post_id)  # Retrieve the post
        return render_template("deletepost.html", post_id = post_id, post = post, form = form, base64 = base64 )
    
    flash("you're not logged in.")
    return redirect(url_for("views.homepage"))
        

@auth.route("/posts/logout", methods = ["GET", "POST"]) #logout route
def logout():
    if 'user_id' in session:
        form = logoutform()
        if request.method == "POST":
            confirmlogout = request.form.get('logout')#confirm logout from form
            if confirmlogout :
                session.pop('user_id')#remove user id from session
                return redirect(url_for("views.homepage"))
            flash("Unable to log out.", category= "error")
            return redirect(url_for('views.posts'))
        return render_template("Logout.html", form = form)# display logout form if request method is get
    flash("you're not logged in.")
    return redirect(url_for("views.homepage"))