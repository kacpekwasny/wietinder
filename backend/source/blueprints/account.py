import os
import json
import time
import random
import string

from flask import Blueprint, request, jsonify, send_from_directory, url_for
from flask_login import current_user
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from werkzeug.utils import secure_filename
from werkzeug.security import safe_join

from ..models import User
from ..tools.files import secure_unique_filename_for_directory


def get_account_bp(db: SQLAlchemy, upload_dir: Path):
    account_bp = Blueprint('views', __name__)

    @account_bp.route('/account-data', methods=['GET'])
    @login_required
    def get_account_data():
        return jsonify(User.get_json(current_user))

    @account_bp.route('/account-data', methods=['POST'])
    @login_required
    def post_account_data():
        j = request.json
        print(json.dumps(j, indent=4))
        try:
            User.set_from_json(current_user, **j)

        except KeyError as e:
            return jsonify({'ok': False, 'info': f'missing key: {e}'})
        
        db.session.commit()
        return get_account_data()
    
    @account_bp.route('/profile/<profile_id>')
    @login_required
    def get_profile(profile_id: str):
        return jsonify(User.query.filter_by(public_id=profile_id)
                       .first_or_404().get_json())
    
    @account_bp.route('/get-images', methods=['GET'])    # moze GET /get-images? albo /profile-images, myśle, że można w domyśle mieć, że to jest GET i nie trzeba go by wtedy dawać z przodu linku.
    @login_required
    def get_images():
        response = {
            "images": User.get_images(current_user)
        }
        return jsonify(response)

    @account_bp.route('/upload-images', methods=['POST'])
    @login_required
    def upload_images():
        files = request.files.getlist('images')
        new_images = []
        print(files)

        for file in files:
            if not (file and allowed_img_extension(file.filename)):
                return jsonify({'ok': False, 'info': 'invalid_file'})
            
            unique_imagename = secure_unique_filename_for_directory(file.filename, directory=upload_dir)
            file.save(str(upload_dir / unique_imagename))
            new_images.append(unique_imagename)
        
        User.set_images(current_user, User.get_images(current_user) + new_images)
        db.session.commit()
       
        return jsonify({'ok': True})


    @account_bp.route('/uploads/<path:filepath>')
    @login_required
    def get_image(filepath: str):
        directory_path = str(Path(__file__).parent.parent.parent / "uploads")
        return send_from_directory(directory_path, filepath)
    
    @account_bp.route('/delete-image', methods=['POST'])
    @login_required
    def delete_image():
        j = request.json
        removedImageName = j["removed_image_name"]
        user_owned_images = User.get_images(current_user)

        if not removedImageName in user_owned_images:
            return jsonify({'ok': False, 'info': "No image found"})
        
        from ..config import UPLOADS_DIR

        try:
            os.remove(safe_join(str(UPLOADS_DIR), removedImageName))
        except OSError as e:
            return jsonify({'ok': False, 'info': "No image found"})
        
        user_owned_images.remove(removedImageName)
        User.set_images(current_user, user_owned_images)
        db.session.commit()

        return jsonify({'ok': True})

    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    def allowed_img_extension(filename: str):
        print(Path(filename).suffix.lower())
        return Path(filename).suffix.lower().replace(".", "") in ALLOWED_EXTENSIONS
       
    return account_bp
