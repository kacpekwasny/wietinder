from flask import Flask, send_from_directory
from werkzeug import exceptions
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from os import path
from flask_login import LoginManager

 
db = SQLAlchemy()
DB_NAME = 'database.db'



def create_app():
   
    

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdfjasdi'
    db_path = path.join(app.root_path, DB_NAME)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    db.init_app(app)

    @app.route('/', defaults={'path': 'index.html'})
    @app.route('/<path:path>')
    def index(path):
        try:
            return send_from_directory('/home/kacper/code/wietinder/dist/', path)
        except exceptions.NotFound:
            return send_from_directory('/home/kacper/code/wietinder/dist/', "index.html")

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
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
