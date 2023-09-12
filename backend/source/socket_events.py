import functools
from typing import Literal
from flask_socketio import emit, disconnect

from . import socketio
from .models import User

AUTH_KEY_JWT_WS = "__flask_auth_jwt_ws"

def login_required_sock(f):
    @functools.wraps(f)
    def wrapped(auth: dict[Literal["jwt"], str], *args, **kwargs):
        jwt = auth.get(AUTH_KEY_JWT_WS, None)
        if jwt is None:
            return disconnect()
        user = User.get_user_by_jwt(jwt)
        if user is None:
            print(f'jwt invalid {jwt=}')
            return disconnect()

        emit('jwt_refresh', {"jwt": user.refresh_jwt()})
        return f(user, *args, **kwargs)
    return wrapped


@socketio.on('connect')
def handle_connect():
    print(f'A user connected')
    

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')