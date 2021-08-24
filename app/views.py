from app import app
from flask import render_template, request, jsonify, make_response
from trie import scrabble
import json

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        json_body = json.loads(request.data.decode('utf-8')) # parse json
        possible_words = scrabble.find_words(json_body['board_dict'], json_body['userLetters'])
        json_response = make_response(jsonify(possible_words), 200)
        return json_response
    return render_template('index.html')

