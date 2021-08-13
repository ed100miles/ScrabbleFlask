from app import app
from flask import render_template, request, jsonify, make_response
from trie import scrabble
import json

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        json_body = json.loads(request.data.decode('utf-8'))
        user_letters = json_body['userLetters']
        board_dict = json_body['board_dict']
        print(board_dict)
        possible_words = scrabble.find_words(board_dict, user_letters)
        json_response = make_response(jsonify(possible_words), 200)
        return json_response
    return render_template('index.html')
