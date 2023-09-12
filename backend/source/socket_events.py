import functools
from typing import Literal
from flask_socketio import emit, disconnect, join_room

from . import socketio
from .models import User

AUTH_KEY_JWT_WS = "__flask_auth_jwt_ws"

def login_required_sock(f):
    @functools.wraps(f)
    def wrapped(auth: dict[Literal["jwt"], str], *args, **kwargs):
        jwt = auth.get(AUTH_KEY_JWT_WS, None)
        if jwt is None:
            return
        user = User.get_user_by_jwt(jwt)
        if user is None:
            print(f'jwt invalid {jwt=}')
            return

        emit('jwt_refresh', {"jwt": user.refresh_jwt()})
        return f(user, *args, **kwargs)
    return wrapped


@socketio.on('enter_my_room')
@login_required_sock
def enter_my_room_sock(user: User, *data: dict):
    join_room(user.public_id)
    return emit('enter_my_room', {'ok': True})


@socketio.on('connect')
def handle_connect():
    print(f'A user connected')
    

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')