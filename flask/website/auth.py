from flask import Blueprint, request, redirect, url_for, render_template, send_from_directory
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)



@auth.route('/login', methods = ['POST'])
def login():
    print("dupa:", request.json)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(password, user.password):
                login_user(user, remember=True)
                pass
            else:
                pass
        else:
            pass

    return '<p>Sign Up<p>'

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return '<p>Logout<p>'

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
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
        new_user = User(email=email, first_name=first_name, password = generate_password_hash(password1, method = 'sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(user, remember=True)

        return redirect(url_for('views.home'))

    return '<p>Sign Up<p>'