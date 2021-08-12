from scrabbleWords import scrabble_words
from datetime import datetime
import pickle

class Trie:
    """Create and populate Trie data structure and find words that can be made with given letters."""

    class _Node:
        """Non-public Node subclass for Trie class"""

        def __init__(self, letter=None, is_word=False):
            """Create Trie node instance"""
            self.letter = letter
            self.is_word = is_word
            self.children = {}

    def __init__(self):
        """Initialise instance of Trie class and set root"""
        self.root = self._Node()

    def add_word(self, word:str):
        """Adds word string to the Trie tree"""
        index_node = self.root
        is_word = False
        for letter_index, letter in enumerate(word):
            if letter not in index_node.children:
                if letter_index == len(word) - 1:    # if iter is last letter
                    is_word = word                   # store whole word in node
                index_node.children[letter] = self._Node(
                    letter, is_word)                 # add new node in child dict
            elif letter_index == len(word) - 1:
                index_node.children[letter].is_word = word
            # move index node to new child
            index_node = index_node.children[letter]

    def find_words(self, user_letters:str):
        """Returns set of words in Trie with matching letters in user_letters string"""
        self.found_words = []   # create or clear list for matching words
        user_letters_dict = {}  # create dict of user letters e.g 'a':3
        for letter in user_letters:
            if letter not in user_letters_dict:
                user_letters_dict[letter] = 1
            else:
                user_letters_dict[letter] += 1
        self._find_words(user_letters_dict)
        return set(self.found_words)    # convert to set to remove any possible duplicates

    # --- Private methods:

    def _find_words(self, user_letters, node=None):
        """Appends to self.found_words list all words added to Trie instance that can be made using user_letters"""
        if node == None:
            node = self.root
        if node.is_word:
            self.found_words.append(node.is_word)
        # Base case:
        if len(node.children) == 0 or sum(user_letters.values()) == 0:
            return
        # else recur down each node.child where node.child in user_letters and count > 0
        for child in node.children:
            if child in user_letters and user_letters[child] > 0:
                user_letters_less_child = user_letters.copy()
                user_letters_less_child[child] -= 1
                self._find_words(user_letters_less_child, node.children[child])




# def populate_scrabble_trie(scrabble_words_file_path):

# trie = Trie()
trie = pickle.load(open('trie.pickle', 'rb'))

print(trie.find_words('cat'))

# board_letters = 'vvfht'
# user_letters = 'sinervlsenrlviser'
# out = []
# start = datetime.now()

# for board_letter in board_letters:
#     test_letters = user_letters + board_letter
#     out.add(tuple(trie.find_words(test_letters)))

# print(len(out))
# print(out)


# for letter in board_letters:
#     user_letters.append(board_letters)
# end = datetime.now()


# for word in words:
#     word_up = word.upper()
#     print(f'{word.capitalize()}: {scrabble_words[word_up]}')

# print(f'Duration: {end - start}')

