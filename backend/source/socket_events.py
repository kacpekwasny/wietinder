from flask_socketio import emit

from . import socketio


@socketio.on('send_message')
def handle_new_message(data):
    # Handle the new message, e.g., save it to the database
    message = data['content']
    print(message)
    # ...

    # Emit the message to all connected clients
    emit('message_received', {'message': message}, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')