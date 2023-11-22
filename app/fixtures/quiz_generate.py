import httpx
import html
import random


def generate_quiz(category_id):
    parameters = {
        'amount': 10,
        'difficulty': 'easy',
        'type': 'multiple',
        'category': category_id
    }

    client = httpx.Client()
    response = client.get("https://opentdb.com/api.php", params=parameters)
    response.raise_for_status()
    api_response = response.json()

    # Initialize a question ID counter
    question_id_counter = 1

    quiz = {
        "title": "category" + category_id + " Quiz",
        "questions": []
    }
    option_ids = ["a", "b", "c", "d"]

    # Loop through the API response and convert it to QUIZZES format
    for api_question in api_response["results"]:

        # mix the correct answer with incorrect ones
        options = api_question["incorrect_answers"]
        correct = random.randint(0, 3)
        options.insert(correct, api_question["correct_answer"])

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
            "correct": option_ids[correct],
        }

        # Append the question to the quiz
        quiz["questions"].append(question)

        # Increment the question ID counter
        question_id_counter += 1

    return quiz
