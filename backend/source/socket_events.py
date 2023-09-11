import functools
from flask_login import current_user
from flask_socketio import emit, disconnect

from . import socketio


def login_required_sock(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            print('Not authenticated attempt to use websocket.')
            return disconnect()
        return f(*args, **kwargs)
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