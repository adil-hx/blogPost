from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd79526b4a69da40429cf53318ada056873e0d684cfe8486c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c21117653:Trucker123@csmysql.cs.cf.ac.uk:3306/c21117653_flask_lab_db'

db = SQLAlchemy()
db.init_app(app)
    
from .views import views
from .auth import auth 


app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

from .models import User, Post, Comment, starRating
    

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
    return app 