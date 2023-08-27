from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from flask_cors import cross_origin
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


from ..agh import AGH_FIELDS_OF_STUDY

def get_data_bp() -> Blueprint:

    data = Blueprint('data', __name__)

    @data.route('/static/agh-fields-of-study')
    def fields_of_study():
        return jsonify(AGH_FIELDS_OF_STUDY)
        
    return data