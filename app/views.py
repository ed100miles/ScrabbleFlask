from app import app
from flask import render_template, request, jsonify, make_response
from trie import trie
import json

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        json_body = json.loads(request.data.decode('utf-8'))
        
        user_letters = json_body['userLetters']
        possible_words = trie.find_words(user_letters)
        json_response = make_response(jsonify(possible_words), 200)
        return json_response
    return render_template('index.html')
