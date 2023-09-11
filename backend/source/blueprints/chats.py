from flask import Blueprint, request
from flask.wrappers import Response
from flask_cors import cross_origin
from flask_login import login_user, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from ..socket_events import socketio
from ..tools.response import resp


MAX_MESSAGES_AT_ONCE = 50

def get_chats_bp(db: SQLAlchemy, is_prod: bool=True) -> Blueprint:
    from ..models import User, Message, PossibleMatch

    chats = Blueprint('chats', __name__)


    @chats.route('/chats', methods=['GET'])
    @login_required
    def get_chats():
        return [
            {
                "profile":  m.get_other_user(current_user.public_id).json(),
                "messages": [msg.json() for msg in m.messages_slice(0, 50)],
            }

            for m in User.my_matches(current_user)
        ]


    @chats.route('/more-messages/<public_id>/<int:index_start>/<int:index_end>', methods=['GET'])
    @login_required
    def more_messages(other_pid: str, index_start: int, index_end: int):
        if index_end - index_start > MAX_MESSAGES_AT_ONCE:
            return resp(400, f"One cannot request so many messages at once. {MAX_MESSAGES_AT_ONCE=}")
        m = PossibleMatch.get_match(current_user.public_id, other_pid)
        if m is None:
            return resp(404, "no chat with this user")
        return m.messages_slice(index_start, index_end)



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


