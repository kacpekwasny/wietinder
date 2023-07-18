import os

from dotenv import load_dotenv
from pathlib import Path

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


BACKEND_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BACKEND_DIR.parent
UPLOADS_DIR = BACKEND_DIR / "uploads"

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    load_dotenv()

    from .config import ConfigDev, ConfigProd

    # Teraz nie tutaj ustawiamy link i haslo do SQL, tylko w objektach w pliku
    # config.py. Także kolejne zmienne do konfiguracji (gdy się pojawią) ustawiamy tam.
    conf = ConfigDev
    if os.getenv("IS_PRODUCTION", "false").lower() == "true":
        # ustaw config pod produkcje, jeżewli zmienna środowiskowa 
        # IS_PRODUCTION=True
        conf = ConfigProd

    app.config.from_object(conf)


    db.init_app(app)

    # Blueprints
    from .blueprints.auth import get_auth_bp
    from .blueprints.account import get_account_bp
    from .blueprints.serve_frontend import get_serve_frontend_bp
    app.register_blueprint(get_serve_frontend_bp())
    app.register_blueprint(get_auth_bp(db))
    app.register_blueprint(get_account_bp(db, UPLOADS_DIR))


    from .models import User, Image

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
    admin.add_view(ModelView(Image, db.session))

    return app

def create_database(db_path: Path, app: Flask):
    if not db_path.exists():
        db.create_all(app=app)
        print("Created database")
