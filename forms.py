from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,EmailField,validators, TextAreaField,BooleanField, FileField,ValidationError
from flask_wtf.file import FileAllowed
import os



def image_file_check(form, field):
        ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'png', 'gif', 'jpeg', 'mov', 'mp4']
        if field.data:
            filename = field.data.filename
            ext = os.path.splitext(filename)[1].lower()[1:]
            if ext not in ALLOWED_IMAGE_EXTENSIONS:
                raise ValidationError('Invalid image format. Allowed formats: mov, mp4, png, jpg, jpeg, gif.')

class Signupform(FlaskForm):
    username = StringField("Username",validators=[validators.length(min = 4,max = 15, message= "Not within required length"), validators.input_required(message="We need your username hun.")])
    Email = EmailField("Email",validators=[validators.input_required(), validators.Email(message = "This is not a valid email address.")])
    password = PasswordField("Password",validators=[validators.input_required(), validators.equal_to("confirm_password", message= "your passwords aren't the same.")])
    confirm_password = PasswordField("Confirm password", validators=[validators.input_required()])
    Submit = SubmitField("Sign up!")


class Loginform(FlaskForm):
    username = StringField("Username")
    Email = EmailField("Email")
    password = PasswordField("Password")
    Submit = SubmitField("Log in")


class Postform(FlaskForm):
    Entry = TextAreaField("Tell me something I dont know..." , validators= [validators.input_required("You need to spill something honey."), validators.length(min = 5,max = 500, message= "Not within required length")])
    File = FileField("Proof or it didn't happen!!", validators= [ FileAllowed(['jpg', 'png', 'gif', 'jpeg', 'mov', 'mp4'], "Only picture and video files are allowed dude.")])
    Submit = SubmitField("Confess!")

class logoutform(FlaskForm):
    logout = BooleanField("You will be redirected to the homepage. Logout?")
    

class deletepostform(FlaskForm):
    deletepost = BooleanField("Delete this post??")
    