from flask import Blueprint, render_template, request


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
    },
#     {
#         "id": 2,
#         "question_text": "What is 1 + 2?",
#         "choices": [
#             {"id": "a", "choice_text": "3"},
#             {"id": "b", "choice_text": "4"},
#             {"id": "c", "choice_text": "5"},
#         ],
#     },
# {
#         "id": 3,
#         "question_text": "What is 3 + 2?",
#         "choices": [
#             {"id": "a", "choice_text": "3"},
#             {"id": "b", "choice_text": "4"},
#             {"id": "c", "choice_text": "5"},

#         ],
#     }
]

@question_page.route('/')
def quiz():
    return render_template('game/question_page.html', quiz_title=quiz_title, questions=questions)

@question_page.route('/submit', methods=['POST'])
def submit_quiz():
    # Process the submitted quiz and show the results
    # Add your logic here...
    return "Quiz submitted!"

