from flask import Blueprint, request, redirect, url_for, render_template, send_from_directory, jsonify
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_cors import cross_origin

auth = Blueprint('auth', __name__)



@auth.route('/login', methods = ['POST'])
def login():
    
    email = request.json.get('email')
    password = request.json.get('password')
    print("dupa:", request.json.get('email'))

    user = User.query.filter_by(email = email).first()
    # print(check_password_hash(user.password, password))
    if check_email_exists(email):
        if user.password == password:
            login_user(user, remember=True)
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'failure'}), 401
    else:
        return jsonify({'status': 'failure'}), 404



@auth.route('/register', methods = ['POST'])

def register():
    print("dupa")
    print(request.json.get('email'))
    
    email = request.json.get('email')
    password = request.json.get('password')
    name = request.json.get("name")
    
    user = User.query.filter_by(email = email).first()
    if check_email_exists(user):
        return jsonify({'message': 'Jest zarejestrowane konto na ten email już'}), 400
    elif len(email) < 5 or len(email) > 50 :
        return jsonify({'message': 'Niepoprawna długość maila'}), 400
    elif len(name) < 2 or len(name) > 50:
        return jsonify({'message': 'Niepoprawna długość imienia'}), 400
    elif password < 8:
        return jsonify({'message': 'Hasło musi miec conajmniej 8 znaków'}), 400
    else:
        new_user = User(email=email, first_name=name, password = password)
        db.session.add(new_user)
        db.session.commit()
        login_user(user, remember=True)

        return jsonify({'message': 'Konto zostało założone'}), 200
    

def check_email_exists(email):
    user = User.query.filter_by(email=email).first()
    return user is not None