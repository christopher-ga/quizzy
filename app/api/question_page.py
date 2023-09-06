from flask import Blueprint, render_template, request, session, redirect, url_for
from app.socket_events import rooms
from app.fixtures.quiz import QUIZZES

QUIZ = QUIZZES[0]

question_page = Blueprint("question_page", __name__)


@question_page.route("/", methods=["POST", "GET"])
def question():
    room = session.get("room", None)
    name = session.get("room", None)
    if not room or room not in rooms:
        return redirect(url_for("join_game_page.join_view"))

    question_num = rooms[room]["question_index"]
    if question_num >= len(QUIZ["questions"]):
        # redirect to scoreboard/end of game results!
        print(rooms[room]["usernames"])
        return redirect(url_for("game_room_page.join_view"))
    return render_template(
        "game/question_page.html",
        quiz_title=QUIZ["title"],
        question=QUIZ["questions"][question_num],
    )
