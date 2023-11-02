# from flask import request
import requests
import html
# import gevent.monkey
# category ids
# general knowledge  9
# comp-sci 18
# animals 27
# geography 22
# art 25

def generate_quiz(category_id):
    parameters = {
        'amount': 10,
        'difficulty': 'easy',
        'type': 'multiple',
        'category': category_id
    }
    response = requests.get("https://opentdb.com/api.php", params=parameters)
    # response.raise_for_status()
    api_response = response.json()

    # Initialize a question ID counter
    question_id_counter = 1

    quiz = {
        "title": "category" + " Quiz",
        "questions": []
    }
    # Loop through the API response and convert it to QUIZZES format
    for api_question in api_response["results"]:

        #sort to mix the correct answer with incorrect ones
        options = sorted(api_question["incorrect_answers"] + [api_question["correct_answer"]])

        #find the correct option
        correct = ""
        option_id = ["a", "b", "c", "d"]
        for num, i in enumerate(options):
            if i == api_question["correct_answer"]:
                correct = option_id[num]
        # print(options, api_question["correct_answer"], correct)

        # Create the question dictionary
        question = {
            "id": question_id_counter,
            "question_text": html.unescape(api_question["question"]),
            "choices": [
                {"id": "a", "choice_text": html.unescape(options[0])},
                {"id": "b", "choice_text": html.unescape(options[1])},
                {"id": "c", "choice_text": html.unescape(options[2])},
                {"id": "d", "choice_text": html.unescape(options[3])},
            ],
            "correct": correct,
        }

        # Append the question to the quiz
        quiz["questions"].append(question)

        # Increment the question ID counter
        question_id_counter += 1

    return quiz

print(generate_quiz(9))