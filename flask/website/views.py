from flask import Blueprint, request, jsonify
from flask_login import current_user
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

# @views.route('/')
# @login_required
# def home():
#     return "<h1>Test</h1>"

@views.route('/account-data', methods = ['POST', 'GET'])
@login_required
def account_data():
    if request.method == 'GET':
        response = {
            "bio": current_user.bio,
            "target": {
                "sex": current_user.sex,
                "activity": current_user.activity
            },
            "college_major": current_user.college_major
        }
        return jsonify(response)

    if request.method == 'POST':
        pass