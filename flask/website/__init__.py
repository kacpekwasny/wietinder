import os

from dotenv import load_dotenv
from pathlib import Path
from werkzeug import exceptions

from flask import Flask, send_from_directory
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


WEBSITE_DIR = Path(__file__).resolve().parent


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    
    load_dotenv()

    from .config import ConfigDev, ConfigProd

    config = ConfigDev
    if os.getenv("IS_PRODUCTION", "False") == "True":
        # ustaw config pod produkcje, jeżewli zmienna środowiskowa 
        # IS_PRODUCTION=True
        config = ConfigProd

    app.config.from_object(config)


    db.init_app(app)
    

    from .serve_frontend import serve_frontend
    from .auth import auth

    app.register_blueprint(serve_frontend, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    admin = Admin(app, name='Admin Page', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Created database")
