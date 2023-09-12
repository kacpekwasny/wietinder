import functools
import time
from flask import Blueprint, request
from flask.wrappers import Response
from flask_socketio import SocketIO, join_room, leave_room
from flask_cors import cross_origin
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import emit, disconnect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from ..socket_events import login_required_sock

from ..tools.response import resp



MAX_MESSAGES_AT_ONCE = 50

def reply(data: dict={}, ok: bool=True, msg: str="") -> dict:
    return data | {
        "ok": ok,

        # how to make something super simple, complicated
        "msg": {
            (True, ''):  'ok',
            (False, ''): 'error',
        }.get((ok, msg), msg),
    }

def room_name(pid1: str, pid2: str) -> str:
    print(pid1, pid2)
    return ''.join(sorted([pid1, pid2]))


def get_chats_bp(db: SQLAlchemy, socketio: SocketIO, is_prod: bool=True) -> Blueprint:
    from ..models import User, Message, PossibleMatch

    chats = Blueprint('chats', __name__)


    @chats.route('/chats-list', methods=['GET'])
    def get_chats():
        return [
            {
                "profile":  m.get_other_user(current_user.public_id).json(),
                "messages": [msg.json() for msg in m.messages_slice(0, 50)],
            }

            for m in User.my_matches(current_user)
        ]

    @socketio.on('get-chats-list')
    def get_chats_sock():
        print('get-chats-list')
        emit('chats-list', 'adw')


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

    @socketio.on('join_room')
    @login_required_sock
    def join_room_sock(user: User, *data: dict):
        data = data[0]
        author_id    = user.public_id
        recepient_id = data["recepient_public_id"]
        pm = PossibleMatch.get_match(author_id, recepient_id)
        if pm is None:
            return emit('join_room', reply(ok=False, msg="not_a_pair"))
        join_room(room_name(author_id, recepient_id))
        return emit('join_room', reply(ok=True))

    @socketio.on('leave_room')
    @login_required_sock
    def leave_room_sock(user: User, *data: dict):
        data = data[0]
        author_id    = user.public_id
        recepient_id = data["recepient_public_id"]
        leave_room(room_name(author_id, recepient_id))
        return emit('leave_room', reply(ok=True))


    @socketio.on('server_message')
    @login_required_sock
    def send_message_sock(user: User, *data: dict):
        data = data[0]
        recepient_id = data["recepient_public_id"]
        author_id    = user.public_id
        print('send message:', data, user)
        pm = PossibleMatch.get_match(author_id, recepient_id)
        msg: Message = Message(
            possible_match_id=pm.id,
            author=author_id,
            timemstamp=time.time(),
            message=data['content']
        )
        emit('client_message',
            msg.json() | {"recepient_id": recepient_id},
            room=room_name(author_id, recepient_id),
        )
        db.session.add(msg)
        db.session.commit()

    return chats


