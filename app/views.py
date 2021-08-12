from app import app
from flask import render_template, request, jsonify, make_response
from trie import trie

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_letters = request.data.decode('utf-8')
        possible_words = trie.find_words(user_letters)
        print(possible_words)
        json_response = make_response(jsonify(possible_words), 200)
        return json_response
    return render_template('index.html')
