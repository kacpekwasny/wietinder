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

from ..tools.response import resp

from ..models import User
from ..tools.files import secure_unique_filename_for_directory
from ..config import UPLOADS_DIR



def get_account_bp(db: SQLAlchemy, upload_dir: Path):
    account_bp = Blueprint('views', __name__)

    @account_bp.route('/account-data', methods=['GET'])
    @login_required
    def get_account_data():
        return jsonify(User.json(current_user))

    @account_bp.route('/account-data', methods=['POST'])
    @login_required
    def post_account_data():
        j: dict = request.json
        j.pop("sex", None)
        try:
            User.set_from_json(current_user, **j)

        except KeyError as e:
            return resp(400, f'missing key: {e}')
        
        db.session.commit()
        return get_account_data()
    
    @account_bp.route('/profile/<profile_id>')
    @login_required
    def get_profile(profile_id: str):
        return jsonify(User.query.filter_by(public_id=profile_id)
                       .first_or_404().json())
    
    @account_bp.route('/upload-images', methods=['POST'])
    @login_required
    def upload_images():
        files = request.files.getlist('images')
        new_images = []

        current_images = User.get_images(current_user)

        if len(current_images) + len(files) > 9:
            return resp(400, 'too_many_images')


        for file in files:
            if not (file and allowed_img_extension(file.filename)):
                return resp(400, 'invalid_file')
            
            unique_imagename = secure_unique_filename_for_directory(file.filename, directory=upload_dir)
            file.save(str(upload_dir / unique_imagename))
            new_images.append(unique_imagename)
        
        User.set_images(current_user, current_images + new_images)
        db.session.commit()
       
        return resp(200)


    @account_bp.route('/uploads/<path:filepath>')
    @login_required
    def get_image(filepath: str):
        directory_path = str(Path(__file__).parent.parent.parent / "uploads")
        return send_from_directory(directory_path, filepath)
    
    @account_bp.route('/delete-image', methods=['POST'])
    @login_required
    def delete_image():
        removed_img_name = request.json["removed_image_name"]
        user_owned_images = User.get_images(current_user)

        if not removed_img_name in user_owned_images:
            return resp(404, "No image found")

        imgpath = safe_join(str(UPLOADS_DIR), removed_img_name)
        if Path(imgpath).exists():
            try:
                os.remove(imgpath)
            except OSError as e:
                return resp(404, "No image found")

        # Checked above the image is contained in the list.
        user_owned_images.remove(removed_img_name)
        User.set_images(current_user, user_owned_images)
        db.session.commit()

        return resp(200)

    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    def allowed_img_extension(filename: str):
        return Path(filename).suffix.lower().replace(".", "") in ALLOWED_EXTENSIONS
       
    return account_bp
