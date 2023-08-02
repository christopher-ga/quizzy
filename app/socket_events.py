from flask_socketio import send
from flask import request

users = []


def define_socket_events(socketio):
    # connect and disconnect are reserved events detected automatically by socketio

    # currently these events are received when client accesses /gameroom

    # when a user connects to the socket do the following
    @socketio.on('connect')
    def test_connect():
        print('CLIENT CONNECTED')
        users.append(request.sid)
        print(users)

    # when a user disconnects from the socket do the following
    @socketio.on('disconnect')
    def disconnect():
        print('CLIENT DISCONNECTED')

        # emit a custom event to ALL connected clients along with an object containing a message
        socketio.emit('user_disconnected', {'message': 'A user has disconnected'})


