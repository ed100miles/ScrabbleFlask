from app import app
from flask import render_template, request, redirect, jsonify, make_response
from trie import trie

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_letters = request.data.decode('utf-8')
        # print(user_letters)
        print(trie.find_words(user_letters))
    return render_template('index.html')
