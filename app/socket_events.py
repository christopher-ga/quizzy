from flask_socketio import send
from flask import request, session

users = []
usernames = set()


def handle_add_user(name, socket_id):
    global users, usernames  # declare users and usernames as global

    user = {
        "username": name,
        "id": socket_id
    }

    usernames.add(user['username'].lower())

    users.append(user)


def handle_delete_user(socket_id):
    target_user = ''

    for i, user in enumerate(users):
        if user['id'] == socket_id:
            target_user = users[i]
            del users[i]

    usernames.discard(target_user['username'])
    return target_user


def define_socket_events(socketio):
    # connect and disconnect are reserved events detected automatically by socketio

    # currently these events are received when client accesses /gameroom

    # when a user connects to the socket do the following
    @socketio.on('connect')
    def test_connect():
        print('CLIENT CONNECTED')
        handle_add_user(session['name'], request.sid)
        print(users)
        print(usernames)

    # when a user disconnects from the socket do the following
    @socketio.on('disconnect')
    def disconnect():
        deleted_user = handle_delete_user(request.sid)
        print(f"{deleted_user['username']} has disconnected")
        print(users)
        print(usernames)

        # emit a custom event to ALL connected clients along with an object containing a message
        socketio.emit('user_disconnected', {'message': f"A {deleted_user} has disconnected"})
