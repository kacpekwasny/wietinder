from flask import Blueprint, request
from flask.wrappers import Response
from flask_cors import cross_origin
from flask_login import login_user, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from ..tools.response import resp

MAX_MESSAGES_AT_ONCE = 50

def get_chats_bp(db: SQLAlchemy, is_prod: bool=True) -> Blueprint:
    from ..models import User, Message, PossibleMatch

    chats = Blueprint('chats', __name__)


    @chats.route('/chats/<int:index_start>/<int:index_end>', methods=['GET'])
    @login_required
    def get_chats(index_start: int, index_end: int):
        if index_end - index_start > MAX_MESSAGES_AT_ONCE:
            return resp(400, f"One cannot request so many messages at once. {MAX_MESSAGES_AT_ONCE=}")
        return {m.get_pairs_public_id(current_user.public_id): m.messages_slice(index_start, index_end)
            for m in User.matches(current_user)}


    @chats.route('/send-message', methods=['POST'])
    @login_required
    def send_message():
        j: dict = request.json
        recepient_pid = j.get("recepient_public_id")
        content       = j.get("content")
        current_user
        match = PossibleMatch.get_match(current_user.public_id, recepient_pid)
        if match is None:
            return resp(404, "you dont have such a match")
        msg = Message(
            possible_match=match,
            author=current_user.public_id,
            message=content,
        )
        db.session.add(msg)
        db.session.commit()

        return resp(200)

    


            
    return chats


