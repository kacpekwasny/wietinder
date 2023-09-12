import functools
from typing import Literal
from flask import g, session
from flask_login import current_user
from flask_socketio import emit, disconnect

from . import socketio
from .models import User

AUTH_KEY_JWT_WS = "__flask_auth_jwt_ws"

def login_required_sock(f):
    @functools.wraps(f)
    def wrapped(auth: dict[Literal["jwt"], str], *args, **kwargs):
        jwt = auth.get(AUTH_KEY_JWT_WS, None)
        if jwt is None:
            print(f'jwt is None. disconnect()')
            return disconnect()
        user = User.get_user_by_jwt(jwt)
        if user is None:
            print(f'jwt invalid {jwt=}')
            return disconnect()

        emit('jwt_refresh', {"jwt": user.refresh_jwt()})
        g._login_user = user
        return f(*args, **kwargs)
    return wrapped




@socketio.on('send_message')
@login_required_sock
def handle_new_message(data):
    # Handle the new message, e.g., save it to the database
    message = data['content']
    print(message)
    # ...

    # Emit the message to all connected clients
    emit('message_received', {'message': message}, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print(f'A user connected')
    

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')