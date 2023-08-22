import os

from flask import Blueprint, request, jsonify, url_for
from flask_login import current_user
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from werkzeug.utils import secure_filename
import time
import random
import string


def get_account_bp(db: SQLAlchemy, upload_dir: Path):
    account_bp = Blueprint('views', __name__)

    @account_bp.route('/account-data', methods=['GET'])
    @login_required
    def get_account_data():
        response = {
            "bio": current_user.bio,
            "my_sex": current_user.sex.value,
            "target_sex": current_user.target_sex.split(";"),
            "target_activity": current_user.target_activity,
            "college_major": current_user.college_major,
            "images": [image.filename for image in current_user.images]
        }
        return jsonify(response)

    @account_bp.route('/account-data', methods=['POST'])
    @login_required
    def post_account_data():
        j = request.json
        print(j)
        try:
            current_user.bio = j["bio"]
            current_user.college_major = j["college_major"]
            current_user.sex = j["my_sex"]
            current_user.target_sex = ";".join(j["target_sex"])
            current_user.target_activity = j["target_activity"]
        except KeyError as e:
            return jsonify({'ok': False, 'info': f'missing key: {e}'})
        
        
            

        db.session.commit()

        return get_account_data()
   
        # file = request.files['image']
        # if not (file and allowed_file(file.filename)):
        #     return jsonify({'ok': False, 'info': 'invalid_file'})
    
        # filename = secure_filename(file.filename)

        # file.save(str(upload_dir / filename))

        # file = Image(filename=filename, user=current_user)
        
        # db.session.add(file)
        # db.session.commit()

        # return jsonify({'ok': True, 'info': 'updated'})

    
    @account_bp.route('/upload-images', methods=['GET'])
    @login_required
    def get_images():
        image_filenames = [image.filename for image in current_user.images]
        response = {
            "images": image_filenames
        }
        return jsonify(response)

    @account_bp.route('/upload-images', methods=['POST'])
    @login_required
    def upload_images():
        files = request.files

        for key, file in files.items():
            if not (file and allowed_file(file.filename)):
                print("dupa")
                return jsonify({'ok': False, 'info': 'invalid_file'})
            imageName = secure_filename(file.filename)
            unique_imagename = generate_unique_image_name(imageName, current_user.email)
            file.save(str(upload_dir / unique_imagename))
            file = Image(filename=unique_imagename, user=current_user)
            db.session.add(file)
        db.session.commit()
       
        return jsonify({'ok': True})

    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    def allowed_file(filename: str):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def generate_unique_image_name(imagename, username):
        timestamp = int(time.time())
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        unique_prefix = f"{timestamp}_{random_string}"
        base_name, extension = os.path.splitext(imagename)
        image_unique_name = unique_prefix + base_name + username + extension
        return image_unique_name

        
    
    return account_bp
