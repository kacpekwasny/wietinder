import functools
from flask import g
from flask_login import current_user
from flask_socketio import emit, disconnect

from . import socketio
from .models import User

def login_required_sock(f):
    @functools.wraps(f)
    def wrapped(data, *args, **kwargs):
        user = User.get_user_by_jwt(data["__flas_auth_jwt"])
        if user is None:
            return disconnect()

        emit('jwt_refresh', {"jwt", user.refresh_jwt()})
        g._login_user = user
        return f(data, *args, **kwargs)
    return wrapped




@socketio.on('send_message')
def handle_new_message(data):
    # Handle the new message, e.g., save it to the database
    message = data['content']
    print(message)
    # ...

    # Emit the message to all connected clients
    emit('message_received', {'message': message}, broadcast=True)

@socketio.on('connect')
@login_required_sock
def handle_connect():
    print(f'{current_user.name} connected')
    

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')