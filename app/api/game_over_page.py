from flask import Blueprint, render_template, request, session, redirect, url_for
from app.socket_events import rooms

game_over_page = Blueprint('game_over_page', __name__)

@game_over_page.route('/gameover')
def game_over():
    final_score = session.get("score", 0)
    return render_template('game/game_over_page.html', final_score=final_score)

