from flask import Blueprint, send_from_directory
from werkzeug import exceptions
from pathlib import Path

DIST = Path(__file__).parent.parent.parent.parent / "frontend/dist"

def get_serve_frontend_bp():
    serve_frontend = Blueprint('serve_frontend', __name__)

    @serve_frontend.route('/', defaults={'path': 'index.html'})
    @serve_frontend.route('/<path:path>')
    def index(path):
        try:
            return send_from_directory(str(DIST), path)
        except exceptions.NotFound:
            return send_from_directory(str(DIST), "index.html")

    return serve_frontend