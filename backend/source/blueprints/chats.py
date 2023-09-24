import functools
import time
from flask import Blueprint, request
from flask_socketio import SocketIO, join_room, leave_room, emit, rooms
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy

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



def get_chats_bp(db: SQLAlchemy, socketio: SocketIO, is_prod: bool=True) -> Blueprint:
    from ..models import User, Message, PossibleMatch

    chats = Blueprint('chats', __name__)


    @chats.route('/api/chats-list', methods=['GET'])
    def get_chats():
        return [
            {
                "profile":  m.get_other_user(current_user.public_id).json(),
                "messages": [msg.json() for msg in m.messages_slice(0, 50)],
                "timestamp": m.matched_timestamp,
            }

            for m in User.my_matches(current_user)
        ]


    @chats.route('/api/more-messages/<public_id>/<int:index_start>/<int:index_end>', methods=['GET'])
    @login_required
    def more_messages(other_pid: str, index_start: int, index_end: int):
        if index_end - index_start > MAX_MESSAGES_AT_ONCE:
            return resp(400, f"One cannot request so many messages at once. {MAX_MESSAGES_AT_ONCE=}")
        m = PossibleMatch.get_match(current_user.public_id, other_pid)
        if m is None:
            return resp(404, "no chat with this user")
        return m.messages_slice(index_start, index_end)


    @socketio.on('client_sends_msg')
    @login_required_sock
    def send_message_sock(user: User, *data: dict):
        data = data[0]
        recepient_id = data["recepient_public_id"]
        author_id    = user.public_id

        content: str = data['content']

        if len(content.strip(" ").replace("\n", "")) == 0:
            return

        pm = PossibleMatch.get_match(author_id, recepient_id)
        if pm is None:
            print('Attempted to send message to a nonexistent match.')
            return

        msg: Message = Message(
            possible_match_id=pm.id,
            author=author_id,
            timemstamp=time.time()*1000,
            message=data['content']
        )
        msg_json = msg.json() | {"recepient_id": recepient_id}

        emit('server_broadcast_message',
            msg_json,
            room=[recepient_id, author_id],
        )
        db.session.add(msg)
        db.session.commit()

    return chats


