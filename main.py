import functions_framework
import requests
import json
import re
import os
from pymongo import MongoClient

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

    insertToMongo(result)

    return "Ok", 200


def insertToMongo(questions):
    # Connect to your MongoDB database
    client = MongoClient(os.environ.get("MONGO_LINK"))

    db = client[os.environ.get("MONGO_DB")]  
    collection = db[os.environ.get("MONGO_COLLECTION")]

    for question in questions:
        collection.insert_one(question)
    
    return

def get_leetcode_question_description(title_slug):
    url = "https://leetcode.com/graphql/"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    body = {
        "query": """
      query QuestionDescription($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
          content
        }
      }
    """,
        "variables": {"titleSlug": title_slug},
    }

    response = requests.post(url, headers=headers, json=body)
    data = json.loads(response.content)

    question_description = str(data["data"]["question"]["content"])

    # Remove all HTML tags.
    description = re.sub(r"<[^>]*>", "", question_description)

    # Remove all HTML entities.
    description = re.sub(r"&[^;]*;", "", description)

    return description


def get_leetcode_question_related_topics(question, desc):
    topics =  [
        "Array",
        "Sorting",
        "Linked List",
        "Two Pointers",
        "Heap",
        "Stack",
        "Queue",
        "Matrix",
        "Back Tracking",
        "Binary Search",
        "Bit Operation",
        "Intervals",
        "Tree",
        "String",
        "Sliding Window",
        "Hash Table",
        "Math",
        "Binary Tree",
        "Greedy",
        "Depth First Search",
        "Breadth First Search",
        "Dynamic Programming",
        "Divide and Conquer",
        "Backtracking",
        "Topological Sort",
        "Trie",
        "Union Find",
        "Quickselect",
        "Monotonic Stack",
        ]

    currq_topics = []
    for item in topics:
        if item in question["stat"]["question__title"] or item.lower() in desc.lower():
            currq_topics.append(item)
    return currq_topics
    

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

        curr_q_desc = get_leetcode_question_description(question["stat"]["question__title_slug"])

        if curr_q_desc == "None":
            continue

        curr_q = {
            "id": question["stat"]["frontend_question_id"],
            "title": question["stat"]["question__title"],
            "difficulty": question["difficulty"]["level"],
            "description": curr_q_desc + f"\n\n Taken from Leetcode! Link: https://leetcode.com/problems/{question['stat']['question__title_slug']}",
            "topics": get_leetcode_question_related_topics(question, curr_q_desc),
        }

        if curr_q["description"] != "None":
            questions.append(curr_q)
            counter += 1

    return questions