import os

from flask import Blueprint, request, jsonify
from flask_login import current_user
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from werkzeug.utils import secure_filename

from ..models import Image


def get_account_bp(db: SQLAlchemy, upload_dir: Path):
    account_bp = Blueprint('views', __name__)

    @account_bp.route('/account-data', methods=['GET'])
    @login_required
    def get_account_data():
        response = {
            "bio": current_user.bio,
            "my_sex": current_user.sex,
            "target": {
                "sex": current_user.target_sex,
                "activity": current_user.target_activity
            },
            "college_major": current_user.college_major,
            "images": current_user.images, # lista linków w odpowiedniej kolejności
        }
        return jsonify(response)

    @account_bp.route('/account-data', methods=['POST'])
    @login_required
    def post_account_data():
        j = request.json
        current_user.bio = j["bio"]
        current_user.college_major = j["college_major"]
        
        db.session.commit()

        return jsonify({'ok': True, 'info': 'updated'})

    # def post_account_data():
    #     file = request.files['image']
    #     if not (file and allowed_file(file.filename)):
    #         return jsonify({'ok': False, 'info': 'invalid_file'})
    
    #     filename = secure_filename(file.filename)

    #     file.save(str(upload_dir / filename))

    #     image = Image(filename=filename, user=current_user)
        
    #     db.session.add(image)
    #     db.session.commit()

    #     return jsonify({'ok': True, 'info': 'updated'})


    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    def allowed_file(filename: str):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    return account_bp
