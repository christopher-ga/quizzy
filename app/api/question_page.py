from flask import Blueprint, render_template, request, session, redirect, url_for
from app.socket_events import rooms

question_page = Blueprint("question_page", __name__)

# Sample quiz data
quiz_title = "My Even More Awesome Quiz"
questions = [
    {
        "id": 1,
        "question_text": "What is 2 + 2?",
        "choices": [
            {"id": "a", "choice_text": "3"},
            {"id": "b", "choice_text": "4"},
            {"id": "c", "choice_text": "5"},
            {"id": "d", "choice_text": "6"},
        ],
        "correct": "b",
    },
    {
        "id": 2,
        "question_text": "What is 1 + 2?",
        "choices": [
            {"id": "a", "choice_text": "3"},
            {"id": "b", "choice_text": "4"},
            {"id": "c", "choice_text": "5"},
        ],
        "correct": "a",
    },
    {
        "id": 3,
        "question_text": "What is 3 + 2?",
        "choices": [
            {"id": "a", "choice_text": "3"},
            {"id": "b", "choice_text": "4"},
            {"id": "c", "choice_text": "5"},
        ],
        "correct": "c",
    },
    {
        "id": 4,
        "question_text": "How many apples did Celina eat",
        "choices": [
            {"id": "a", "choice_text": "1"},
            {"id": "b", "choice_text": "Too many"},
            {"id": "c", "choice_text": "6"},
            {"id": "c", "choice_text": "5"},
        ],
        "correct": "a",
    },
]


@question_page.route("/waiting")
def waiting():
    return render_template("game/waiting_page.html")


@question_page.route("/", methods=["POST", "GET"])
def quiz():
    room = session["room"]
    num = rooms[room]["num"]
    return render_template(
        "game/question_page.html", quiz_title=quiz_title, question=questions[num]
    )


@question_page.route("/submit", methods=["POST"])
def submit_quiz():
    room = session["room"]
    num = rooms[room]["num"]
    name = session["name"]
    print()
    # Process the submitted quiz and show the results
    # Add your logic here...
    # print(session["name"])
    id = str(questions[num]["id"])
    print("HELLO")
    print(questions[num]["correct"])
    print(request.form)
    print(request.form.value)
    if request.form["value"] == questions[num]["correct"]:
        print("updating score")
        session["score"] += 1
        rooms[room]["usernames"][name]["score"] += 1
    rooms[room]["current_round_num"] += 1
    # if question pool exhausted, go back to main menu
    if num == len(questions) - 1:
        return redirect(url_for("game_room_page.join_view"))

    return "Blah"
