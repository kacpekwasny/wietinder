from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from flask_cors import cross_origin
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


def resp(code: int, info=None) -> tuple[Response, int]:
    ok = code == 200
    data = dict(ok=ok)

    if isinstance(info, str):
        data |= dict(info=info)

    return jsonify(data), code

def get_auth_bp(db: SQLAlchemy, is_prod: bool=True) -> Blueprint:
    from ..models import User

    auth = Blueprint('auth', __name__)

    def check_email_exists(email):
        user = User.query.filter_by(email=email).first()
        return user is not None

    @auth.route('/login', methods=['POST'])
    def login():
        email = request.json.get('email')
        password = request.json.get('password')
        
        user = User.query.filter_by(email = email).first()
        if check_email_exists(email):
            if check_password_hash(user.password, password):
                if login_user(user, remember=True):
                    return resp(200)
        
                return resp(500, "unknown_fail")

            else:
                return resp(401, "password_missmatch")
        else:
            return resp(404, "email_not_registered")

    @auth.route('/login')
    def get_login():
        return """

        <input id="e">
        <input id="p">
        <button onclick="postLogin()">awd</button>
        
        <script>
        e = document.getElementById("e");
        p = document.getElementById("p");
        
        function postLogin() {
            object = {
                "email": e.value,
                "password": p.value,
            }

            fetch("/login", {
                method: "POST", headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(object),
                credentials: "same-origin",
        }).then(console.log)
        }


        </script>

        """


    @auth.route('/register', methods=['POST'])
    def register():
        email = request.json.get('email')
        password = request.json.get('password')
        name = request.json.get("name")
        

        if is_prod:
            # dont check for development
            if check_email_exists(email):
                return resp(400, 'email_registered')

            if len(email) < 5 or len(email) > 50 :
                return resp(400, "email_bad")

            if len(name) < 2 or len(name) > 50:
                return resp(400, "name_len_bad")

            if not name.isalpha():
                return resp(400, "name_alpha_bad")

            if len(password) < 8:
                return resp(400, "password_len_bad")

        new_user = User(email=email,
                        first_name=name,
                        password=generate_password_hash(password,
                                                        method='pbkdf2:sha1',
                                                        salt_length=8))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)

        return resp(200)
    
    return auth


