import eventlet
from flask_socketio import send, join_room, leave_room
from flask import request, session

eventlet.monkey_patch()

rooms = {} # dict of room codes containing user data

def start_timer(socketio, room):
    t = 10
    while t:
        eventlet.sleep(1)
        t -= 1
        socketio.emit('room_filled', t, to=room)


def update_users(socketio, room):
    if room in rooms:
        socketio.emit('update_players', {'names': list(rooms[room]["usernames"])}, to=room)


def define_socket_events(socketio):
    # connect and disconnect are reserved events detected automatically by socketio

    # currently these events are received when client accesses /gameroom

    # when a user connects to the socket do the following
    @socketio.on('connect')
    def test_connect():
        room = session.get("room")
        name = session.get("name")
        if not room or not name:
            return
        if room not in rooms:
            leave_room(room)
            return
        join_room(room)

        send({"name": name, "message": "has entered the room"}, to=room)

        # when there are two users in the game_room_page, start a timer
        if len(rooms[room]["usernames"]) == 2:
            print('2 users on now')
            eventlet.spawn(start_timer, socketio, room)

        # update list of players on game page
        eventlet.spawn(update_users, socketio, room)

    # when a user disconnects from the socket do the following
    @socketio.on('disconnect')
    def disconnect():
        room = session.get("room")
        name = session.get("name")
        leave_room(room)

        if room in rooms and name in rooms[room]["usernames"]:
            rooms[room]["usernames"].remove(name) # remove user from room

        # emit a custom event to ALL connected clients along with an object containing a message
        socketio.emit('user_disconnected', {'message': f"A {name} has disconnected"}, to=room)
        eventlet.spawn(update_users, socketio, room)
