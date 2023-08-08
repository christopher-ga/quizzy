from flask import Blueprint, render_template, request, session, url_for, redirect
from app.socket_events import usernames

# join_game blueprint for landing page of app
# should maintain logic over joining quiz queue and redirection to game_room

join_game_page = Blueprint('join_game_page', __name__)


def handle_check_user_exists(username):
    if username in usernames:
        return render_template('game/join_game_page.html', error='Username already exists, please list another name')


@join_game_page.route('/', methods=['POST', 'GET'])
def join_view():
    # receives POST request from form listed in join_game_page.html
    if request.method == 'POST':

        # if name input is provided log the name, store data in session object, redirect user
        # else no name, display current template and send error to template
        name = request.form.get('name')
        if name:
            if name.lower() in usernames:
                return render_template('game/join_game_page.html', error='Username already exists, please list another name')
        else:
            return render_template('game/join_game_page.html', error='Please provide a name')

        session["name"] = name
        session["score"] = 0

        return redirect(url_for('game_room_page.join_view'))

    return render_template('game/join_game_page.html')
