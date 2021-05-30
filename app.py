import time
import requests
import json

import redis
from flask import Flask, jsonify, request, make_response
from flask_api import status
from marshmallow import Schema, fields, ValidationError


class PlaySchema(Schema):
    player = fields.Integer(required=True)


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


GAME_OPTIONS = [
    {"id": 1, "value": "rock"},
    {"id": 2, "value": "paper"},
    {"id": 3, "value": "scissors"},
    {"id": 4, "value": "lizard"},
    {"id": 5, "value": "spock"}
]



def get_random_number():
    number = ""
    URL = "https://codechallenge.boohma.com/random"
    response = requests.get(URL)
    if response.status_code == 200:
        content = json.loads(response.content.decode('utf-8'))
        number = content.get("random_number","") % 5
    return number


def get_all_options():
    return GAME_OPTIONS


def get_record_by_id(id):
    for item in GAME_OPTIONS:
        if item.get("id") == id:
            return item


@app.route('/choices', methods=['GET'])
def get_choices():
    response = get_all_options()
    return make_response(jsonify(response), status.HTTP_200_OK)


@app.route('/choice', methods=['GET'])
def get_random_choice():
    response = get_record_by_id(get_random_number())
    return make_response(jsonify(response), status.HTTP_200_OK)



def get_result(user, computer):
    options = {
        'scissors': ('paper', 'lizard'),
        'paper': ('rock', 'spock'),
        'rock': ('lizard', 'scissors'),
        'lizard': ('spock', 'paper'),
        'spock': ('scissors', 'rock')
    }
    if user==computer:
        return "tie"
    elif computer in options.get(user,[]):
        return "win"
    else:
        return "lose"


@app.route('/play', methods=['POST'])
def play_game():
    request_data = request.json
    schema = PlaySchema()
    try:
        # Validate request body against schema data types
        result = schema.load(request_data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return make_response(jsonify(err.messages), status.HTTP_400_BAD_REQUEST)

    if request_data.get("player")>5 or request_data.get("player")<1:
        return make_response(jsonify({"player": ["choice must between 1 to 5"]}), status.HTTP_400_BAD_REQUEST)

    computer_rec = get_record_by_id(get_random_number())
    user_rec = get_record_by_id(int(request_data.get("player")))

    result = get_result(user_rec.get("value"),computer_rec.get("value"))

    cache.lpush('ScoreBoard', result)

    return make_response(jsonify(result), status.HTTP_200_OK)



@app.route('/scoreboard', methods=['GET'])
def get_score():
    score = {}
    for i in range(0, min(cache.llen("ScoreBoard"),5)):
        result = (cache.lindex("ScoreBoard", i)).decode('utf-8')
        if result in score:
            score[result]+=1
        else:
            score[result] = 1

    return make_response(jsonify(score), status.HTTP_200_OK)


@app.route('/reset-score', methods=['GET'])
def reset_score():
    cache.delete("ScoreBoard")

    return make_response(jsonify("Scoreboard has been successfully reset!"), status.HTTP_200_OK)