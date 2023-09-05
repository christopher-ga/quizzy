from flask import Blueprint, render_template, request, session, redirect, url_for
from app.socket_events import rooms
from app.fixtures.quiz import QUIZZES

QUIZ = QUIZZES[0]

question_page = Blueprint("question_page", __name__)


@question_page.route("/", methods=["POST", "GET"])
def question():
    room = session["room"]
    name = session["name"]
    if room not in rooms:
        return render_template("game/join_game_page.html")

    question_num = rooms[room]["question_index"]
    if question_num >= len(QUIZ["questions"]):
        # redirect to scoreboard/end of game results!
        print(rooms[room]["usernames"])
        return render_template("game/game_room_page.html")
    return render_template(
        "game/question_page.html",
        quiz_title=QUIZ["title"],
        question=QUIZ["questions"][question_num],
    )


@question_page.route("/leaderboard", methods=["GET"])
def leaderboard():
    room = session["room"]
    print('load leaderboard')
    return render_template("game/leaderboard.html", usernames=rooms[room]["usernames"])
