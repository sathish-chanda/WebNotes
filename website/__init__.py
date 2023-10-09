from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    print("Creating the Flask app - {name}".format(name = __name__))
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hdskfjksdgfoeemfdkfdl lldfjeejfenfejfj'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    
    from .models import  User, Note

    with app.app_context():
        db.create_all()
        print("Created Database!!!")

    loginManager = LoginManager()
    loginManager.login_view = 'auth.login'
    loginManager.init_app(app)

    @loginManager.user_loader 
    def load_user(id):
        return User.query.get(int(id))
    
    return app