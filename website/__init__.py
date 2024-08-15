from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "SECRET_KEY_1234"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)


    from .views import views
    from .auth import auth
    from .user_settings import user_settings
    from .models import User

    app.register_blueprint(auth, urlprefix="/")
    app.register_blueprint(views, urlprefix="/")
    app.register_blueprint(user_settings, urlprefix="/profiles")

    with app.app_context():
        create_database()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database():
    if not path.exists("website/"+DB_NAME):
        db.create_all()
        print("Database Created.")