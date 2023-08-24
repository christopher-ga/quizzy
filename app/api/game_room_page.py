from flask import Blueprint, render_template, request, session, redirect, url_for
from app.socket_events import rooms


# game_room blueprint for main game room of quiz game
# currently for testing socket connections
# look at game_room_page.html for socket example

game_room_page = Blueprint('game_room_page', __name__)


@game_room_page.route('/', methods=['POST', 'GET'])
def join_view():
    room = session.get("room")
    name = session.get("name")
    if room == None or name == None or room not in rooms:
        return redirect(url_for("join_game_page.join_view"))
    rooms[room]["usernames"].add(name)
    return render_template('game/game_room_page.html', usernames=rooms[room]["usernames"], code=room)
