from flask import Blueprint, render_template, request, session, redirect, url_for
from app.socket_events import rooms
from app.fixtures.question_setA import quiz

question_page = Blueprint("question_page", __name__)


@question_page.route("/waiting")
def waiting():
    return render_template("game/waiting_page.html")


@question_page.route("/", methods=["POST", "GET"])
def question():
    room = session["room"]
    name = session["name"]

    question_num = rooms[room]["num"]
    if question_num >= len(quiz["questions"]):
        print(rooms[room]["usernames"])
        return render_template("game/game_room_page.html")
        # redirect to scoreboard/end of game results!
        pass
    return render_template(
        "game/question_page.html",
        quiz_title=quiz["title"],
        question=quiz["questions"][question_num],
    )
