import eventlet
from flask_socketio import send, join_room, leave_room
from flask import request, session

from app.fixtures.question_setA import quiz

eventlet.monkey_patch()

rooms = {}  # dict of room codes containing user data


def next_page(socketio, room):
    socketio.emit("next_page", to=room)


def next_question(socketio, room):
    if rooms[room]["num"] < len(quiz["questions"]):
        rooms[room]["num"] += 1
        socketio.emit("next_question", to=room)


def start_timer(socketio, room):
    t = 10

    while t:
        active_users = determine_active_users(room)
        if active_users < 2:
            socketio.emit("reset_timer", to=room)
            break

        eventlet.sleep(1)
        t -= 1
        socketio.emit("room_filled", t, to=room)

    active_users = determine_active_users(room)
    if active_users >= 2:
        eventlet.spawn(next_page, socketio, room)


def update_users(socketio, room):
    if room in rooms:
        active_users = []

        for name, user_data in rooms[room]["usernames"].items():
            if user_data["active"]:
                active_users.append(name)

        socketio.emit("update_players", {"names": active_users}, to=room)


def determine_active_users(room):
    if room not in rooms:
        return 0

    num_active = 0

    for name, user_data in rooms[room]["usernames"].items():
        if user_data["active"]:
            num_active += 1

    return num_active


def define_socket_events(socketio):
    # connect and disconnect are reserved events detected automatically by socketio

    # currently these events are received when client accesses /gameroom

    # when a user connects to the socket do the following
    @socketio.on("connect")
    def test_connect():
        room = session.get("room")
        name = session.get("name")
        if not room or not name:
            print(f"room {room} - name: {name}")
            return
        if room not in rooms:
            print(f"user {name} tried to access room {room}, which doesn't exist")
            leave_room(room)
            return
        join_room(room)

        print(f"{name} has entered the room {room} ")
        send({"name": name, "message": "has entered the room"}, to=room)

        # on connection, set active status to true
        if room in rooms and name in rooms[room]["usernames"]:
            pass
            rooms[room]["usernames"][name]["active"] = True

        # when there are two users in the game_room_page, start a timer
        if len(rooms[room]["usernames"]) == 2:
            print("2 users on now")
            eventlet.spawn(start_timer, socketio, room)

        # update list of players on game page
        eventlet.spawn(update_users, socketio, room)

    # when a user disconnects from the socket do the following
    @socketio.on("disconnect")
    def disconnect():
        room = session.get("room")
        name = session.get("name")
        leave_room(room)

        if room in rooms and name in rooms[room]["usernames"]:
            pass
            rooms[room]["usernames"][name]["active"] = False
            # rooms[room]["usernames"].remove(name) # remove user from room

        # emit a custom event to ALL connected clients along with an object containing a message
        socketio.emit(
            "user_disconnected", {"message": f"A {name} has disconnected"}, to=room
        )
        eventlet.spawn(update_users, socketio, room)

    @socketio.on("user_answer")
    def ready(question, answer):
        room = session.get("room")
        name = session.get("name")
        print(name)
        print(answer)

        def handle_user_response():
            current_question = rooms[room]["num"]
            if answer == quiz["questions"][current_question]["correct"]:
                rooms[room]["usernames"][name]["score"] += 1

        def update_game_status():
            rooms[room]["replies"] += 1
            if rooms[room]["replies"] == len(rooms[room]["usernames"]):
                print("All users have responded")
                # reset replies for next round
                rooms[room]["replies"] = 0
                eventlet.spawn(next_question, socketio, room)

        handle_user_response()
        update_game_status()
