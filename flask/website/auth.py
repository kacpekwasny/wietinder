from flask import Blueprint, request, redirect, url_for, render_template, send_from_directory, jsonify
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)



@auth.route('/login', methods = ['POST'])
def login():
    
    email = request.json.get('email')
    password = request.json.get('password')
    print("dupa:", request.json.get('email'))

    user = User.query.filter_by(email = email).first()
    print(check_password_hash(user.password, password))
    if check_email_exists(email):
        if user.password == password:
            login_user(user, remember=True)
            return jsonify({'status': 'success'})
        else:
            print("dupa")
            return jsonify({'status': 'failure'})
    else:
        print("dupa")
        return jsonify({'status': 'failure'})


@auth.route('/logout')
@login_required
def logout():
    logout_user()


@auth.route('/register', methods = ['POST'])
def sign_up():
    
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    second_name = request.form.get('second_name')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    
    user = User.query.filter_by(email = email).first()
    if user:
        pass
    elif len(email) < 4:
        pass
    elif len(first_name) < 2:
        pass
    elif len(second_name) < 2:
        pass
    elif password2 != password1:
        pass
    else:
        new_user = User(email=email, first_name=first_name, password = password1)
        db.session.add(new_user)
        db.session.commit()
        login_user(user, remember=True)

        return redirect(url_for('views.home'))

def check_email_exists(email):
    user = User.query.filter_by(email=email).first()
    return user is not None