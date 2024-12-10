#import flask
from flask import Flask
from flask_session import Session
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect

#define app
app = Flask(__name__)
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['WTF_CSRF_SSL_STRICT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config["SESSION_TYPE"] = "filesystem"
csrf = CSRFProtect(app)
Session(app)
prefix = '/diary'

# Register auth blueprint with /diary prefix
from auth import auth
app.register_blueprint(auth, url_prefix= prefix)

# Register views blueprint with /diary prefix
from views import views
app.register_blueprint(views, url_prefix= prefix )

# Print available routes
#print(app.url_map)

# Run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
