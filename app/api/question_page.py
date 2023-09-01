from flask import Blueprint, render_template, request, session, redirect, url_for
from app.socket_events import rooms
import eventlet


from app.socket_events import start_question_timer, rooms

question_page = Blueprint('question_page', __name__)

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
        "correct": "b"
    },
    {
        "id": 2,
        "question_text": "What is 1 + 2?",
        "choices": [
            {"id": "a", "choice_text": "3"},
            {"id": "b", "choice_text": "4"},
            {"id": "c", "choice_text": "5"},
        ],
        "correct": "a"
    },
    {
        "id": 3,
        "question_text": "What is 3 + 2?",
        "choices": [
            {"id": "a", "choice_text": "3"},
            {"id": "b", "choice_text": "4"},
            {"id": "c", "choice_text": "5"},

        ],
        "correct": "c"
    },
    {
        "id": 3,
        "question_text": "How many apples did Celina eat",
        "choices": [
            {"id": "a", "choice_text": "1"},
            {"id": "b", "choice_text": "Too many"},
            {"id": "c", "choice_text": "6"},
            {"id": "c", "choice_text": "5"},

        ],
        "correct": "a"
    }
]


@question_page.route('/waiting')
def waiting():
    return render_template('game/waiting_page.html')


@question_page.route('/', methods=["POST", "GET"])
def quiz():
    from app import socketio

    room = session['room']
    num = rooms[room]['num']

    example = session.get("room")

    eventlet.spawn(start_question_timer, socketio, example)  # Call start_question_timer function
    return render_template('game/question_page.html', quiz_title=quiz_title, question=questions[num])


@question_page.route('/submit', methods=['POST'])
def submit_quiz():
    room = session['room']
    num = rooms[room]['num']
    name = session["name"]

    # Process the submitted quiz and show the results
    # Add your logic here...
    # print(session["name"])
    id = str(questions[num]["id"])
    if request.form[id] == questions[num]["correct"]:
        session["score"] += 1
        rooms[room]['usernames'][name]['score'] += 1
    print(session)
    rooms[room]['current_round_num'] += 1
    print(f"username length: {rooms[room]['usernames']}")

    # if question pool exhausted, go back to main menu
    if num == len(questions) - 1:
        return redirect(url_for('game_room_page.join_view'))
    elif rooms[room]['current_round_num'] == len(rooms[room]["usernames"]):
        # All users have answered. Increment num
        rooms[room]['num'] += 1
        rooms[room]['current_round_num'] = 0

    return redirect(url_for('question_page.waiting'))
