import os

from dotenv import load_dotenv
from pathlib import Path

from flask import Flask, Request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

IS_PROD = os.getenv("IS_PRODUCTION", "false").lower() == "true"

def create_app():
    app = Flask(__name__)
    
    load_dotenv()

    from .config import ConfigDev, ConfigProd, UPLOADS_DIR

    # Teraz nie tutaj ustawiamy link i haslo do SQL, tylko w objektach w pliku
    # config.py. Także kolejne zmienne do konfiguracji (gdy się pojawią) ustawiamy tam.
    conf = ConfigDev
    if IS_PROD:
        # ustaw config pod produkcje, jeżewli zmienna środowiskowa 
        # IS_PRODUCTION==True
        conf = ConfigProd

    app.config.from_object(conf)


    db.init_app(app)

    # Blueprints
    from .blueprints.auth import get_auth_bp
    from .blueprints.account import get_account_bp
    from .blueprints.serve_frontend import get_serve_frontend_bp
    from .blueprints.match import get_match_bp
    from .blueprints.data import get_data_bp
    app.register_blueprint(get_serve_frontend_bp())
    app.register_blueprint(get_auth_bp(db, is_prod=IS_PROD))
    app.register_blueprint(get_account_bp(db, UPLOADS_DIR))
    app.register_blueprint(get_match_bp(db))
    app.register_blueprint(get_data_bp())


    from .models import User, PossibleMatch

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id_: str):
        return User.query.get(int(id_))
    

    admin = Admin(app, name='Admin Page', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(PossibleMatch, db.session))

    return app

def create_database(db_path: Path, app: Flask):
    if not db_path.exists():
        db.create_all(app=app)
        print("Created database")
