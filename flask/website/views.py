from flask import Blueprint, request, jsonify
from flask_login import current_user
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Image
from . import UPLOAD_FOLDER, db
import os


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
            "college_major": current_user.college_major,
            # "images": current_user.images
        }
        return jsonify(response)

    if request.method == 'POST':
        file = request.files['image']
        if not (file and allowed_file(file.filename)):
            return jsonify({'ok': False, 'info': 'invalid_file'})
    
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        image = Image(filename=filename, user=current_user)
        db.session.add(image)
        db.session.commit()
        return jsonify({'ok': True, 'info': 'updated'})



ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS