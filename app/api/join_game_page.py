from flask import Blueprint, render_template, request, session, url_for, redirect
import random
from string import ascii_uppercase
from app.socket_events import rooms

# join_game blueprint for landing page of app
# should maintain logic over joining quiz queue and redirection to game_room

join_game_page = Blueprint('join_game_page', __name__)

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code

@join_game_page.route('/', methods=['POST', 'GET'])
def join_view():
    # receives POST request from form listed in join_game_page.html
    if request.method == 'POST':

        # if name input is provided log the name, store data in session object, redirect user
        # else no name, display current template and send error to template
        name = request.form.get('name').lower()
        code = request.form.get("code").upper()
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name and not code:
            if session.get('room') and rooms.get(session['room']):
                return redirect(url_for(rooms[session['room']]['page']))
            else:
                return render_template('game/join_game_page.html', error="You have no active games!", code=code, name=name)

        if not name:
            return render_template('game/join_game_page.html', error="Please enter a name.", code=code, name=name)

        # the following if statement is never true. clicking join with a name but no room code returns line 57
        if join and not code:
            return render_template("game/join_game_page.html", error="Please enter a room code.", code=code, name=name)

        room = code

        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {'usernames': {}}
            rooms[room]['usernames'] = {name: {'score': 0, 'active': True}}
            rooms[room]['replies'] = 0
            rooms[room]['num'] = 0
            rooms[room]['current_round_num'] = 0
            rooms[room]['page'] = 'game_room_page.join_view'
        elif code not in rooms:
            return render_template("game/join_game_page.html", error="Room does not exist.", code=code, name=name)
        elif len(rooms[code]['usernames']) == 5:
            return render_template('game/join_game_page.html', error='Room already full! Join a different room or start your own.')
        elif name.lower() in rooms[room]["usernames"]:
            return render_template('game/join_game_page.html', error='Name already in use in that room, please enter a different name.')

        session["name"] = name.lower()
        session["room"] = room
        session["score"] = 0

        return redirect(url_for('game_room_page.join_view'))

    num_players = len(usernames)
    return render_template('game/join_game_page.html', num_players=num_players)
