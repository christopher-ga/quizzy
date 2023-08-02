from flask import Blueprint, render_template, request


# game_room blueprint for main game room of quiz game
# currently for testing socket connections
# look at game_room_page.html for socket example

game_room_page = Blueprint('game_room_page', __name__)


@game_room_page.route('/', methods=['POST', 'GET'])
def join_view():
    return render_template('game/game_room_page.html')


