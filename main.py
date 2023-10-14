import functions_framework
import requests
import json
import re

@functions_framework.http
def run(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    number = 10

    if request_json and 'number' in request_json:
        number = request_json['number']
    
    result = fetch_leetcode_questions(number)

    return result, 200, {'Content-Type': 'application/json'}




def get_leetcode_question_description(title_slug):
    url = "https://leetcode.com/graphql/"
    headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
    }

    body = {
    "query": """
      query QuestionDescription($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
          content
        }
      }
    """,
    "variables": {
      "titleSlug": title_slug
    }
    }

    response = requests.post(url, headers=headers, json=body)
    data = json.loads(response.content)

    question_description = str(data["data"]["question"]["content"])

    # Remove all HTML tags.
    description = re.sub(r'<[^>]*>', '', question_description)

    # Remove all HTML entities.
    description = re.sub(r'&[^;]*;', '', description)

    return description


def fetch_leetcode_questions(n=10):
    counter = 0
    url = "https://leetcode.com/api/problems/all"

    params = {"isPremium": False}
    response = requests.get(url, params=params)
    data = json.loads(response.content)

    questions = []
    for question in data["stat_status_pairs"]:
        if counter >= n:
            break

        print(question["stat"]["frontend_question_id"])
        curr_q = {
            "id": question["stat"]["frontend_question_id"],
            "title": question["stat"]["question__title"],
            "category": question["stat"]["question__title_slug"],
            "complexity": question["difficulty"]["level"],
            "description" : get_leetcode_question_description(question["stat"]["question__title_slug"]),
            "link": "https://leetcode.com/problems/" + question["stat"]["question__title_slug"]
        }
        print(curr_q["description"])
        print(counter)
        if curr_q["description"] != "None":
            questions.append(curr_q)
            counter += 1

    return questions