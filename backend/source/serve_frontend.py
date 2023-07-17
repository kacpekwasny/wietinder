from flask import Blueprint, send_from_directory
from werkzeug import exceptions

def get_serve_frontend_bp():
    serve_frontend = Blueprint('serve_frontend', __name__)

    @serve_frontend.route('/', defaults={'path': 'index.html'})
    @serve_frontend.route('/<path:path>')
    def index(path):
        try:
            return send_from_directory('../../dist/', path)
        except exceptions.NotFound:
            return send_from_directory('../../dist/', "index.html")

    return serve_frontend