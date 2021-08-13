from scrabbleWords import scrabble_words
from datetime import datetime, time


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

    def add_word(self, word: str):
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

    def find_words(self, user_letters: str):
        """Returns dict of words in Trie with matching letters in user_letters string.
            Dict comprised of matching words as keys and definitions as values."""
        self.found_words = []   # create or clear list for matching words
        user_letters_dict = {}  # create dict of user letters e.g 'a':3
        for letter in user_letters:
            if letter not in user_letters_dict:
                user_letters_dict[letter] = 1
            else:
                user_letters_dict[letter] += 1
        self._find_words(user_letters_dict)
        found_words_and_defs = {}   # convert to dict
        for word in self.found_words:
            word_up = word.upper()
            found_words_and_defs[word] = scrabble_words[word_up]
        return found_words_and_defs

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


trie = Trie()


# populate with scrabble words
for word in scrabble_words:
    trie.add_word(word.lower())


user_letters = 'catukvbktioyfckytcvkytcc'
board = {'0': 'A', '1': 'F', '2': 'S', '3': 'D', '4': 'A', '5': '.', '6': '.', '7': '.', '8': '.', '9': '.', '10': '.', '11': '.', '12': '.', '13': '.', '14': '.', '15': '.', '16': '.', '17': '.', '18': '.', '19': '.', '20': '.', '21': '.', '22': '.', '23': '.', '24': '.', '25': '.', '26': '.', '27': '.', '28': '.', '29': '.', '30': '.', '31': '.', '32': '.', '33': '.', '34': '.', '35': '.', '36': '.', '37': '.', '38': '.', '39': '.', '40': '.', '41': '.', '42': '.', '43': '.', '44': '.', '45': '.', '46': '.', '47': '.', '48': '.', '49': '.', '50': '.', '51': '.', '52': '.', '53': '.', '54': '.', '55': '.', '56': '.', '57': '.', '58': '.', '59': '.', '60': '.', '61': '.', '62': '.', '63': '.', '64': '.', '65': '.', '66': '.', '67': '.', '68': '.', '69': '.', '70': '.', '71': '.', '72': '.', '73': '.', '74': '.', '75': '.', '76': '.', '77': '.', '78': '.', '79': '.', '80': '.', '81': '.', '82': '.', '83': '.', '84': '.', '85': '.', '86': '.', '87': '.', '88': '.', '89': '.', '90': '.', '91': '.', '92': '.', '93': '.', '94': '.', '95': '.', '96': '.', '97': '.', '98': '.', '99': '.', '100': '.', '101': '.', '102': '.', '103': '.', '104': '.', '105': '.', '106': '.', '107': '.', '108': '.', '109': '.', '110': '.', '111': '.', '112': '.', '113': '.', '114': '.', '115': '.', '116': '.',
         '117': '.', '118': '.', '119': '.', '120': '.', '121': '.', '122': '.', '123': '.', '124': '.', '125': '.', '126': '.', '127': '.', '128': '.', '129': '.', '130': '.', '131': '.', '132': '.', '133': '.', '134': '.', '135': '.', '136': '.', '137': '.', '138': '.', '139': '.', '140': '.', '141': '.', '142': '.', '143': '.', '144': '.', '145': '.', '146': '.', '147': '.', '148': '.', '149': '.', '150': '.', '151': '.', '152': '.', '153': '.', '154': '.', '155': '.', '156': '.', '157': '.', '158': '.', '159': '.', '160': '.', '161': '.', '162': '.', '163': '.', '164': '.', '165': '.', '166': '.', '167': '.', '168': '.', '169': '.', '170': '.', '171': '.', '172': '.', '173': '.', '174': '.', '175': '.', '176': '.', '177': '.', '178': '.', '179': '.', '180': '.', '181': '.', '182': '.', '183': '.', '184': '.', '185': '.', '186': '.', '187': '.', '188': '.', '189': '.', '190': '.', '191': '.', '192': '.', '193': '.', '194': '.', '195': '.', '196': '.', '197': '.', '198': '.', '199': '.', '200': '.', '201': '.', '202': '.', '203': '.', '204': '.', '205': '.', '206': '.', '207': '.', '208': '.', '209': '.', '210': '.', '211': '.', '212': '.', '213': '.', '214': '.', '215': '.', '216': '.', '217': '.', '218': '.', '219': '.', '220': '.', '221': '.', '222': '.', '223': '.', '224': '.'}
board2 = {'0': '.', '1': '.', '2': '.', '3': 'E', '4': 'R', '5': 'G', '6': 'V', '7': 'E', '8': 'R', '9': 'G', '10': '.', '11': '.', '12': '.', '13': 'S', '14': '.', '15': '.', '16': '.', '17': '.', '18': '.', '19': '.', '20': '.', '21': 'O', '22': '.', '23': '.', '24': '.', '25': '.', '26': 'S', '27': '.', '28': 'E', '29': '.', '30': '.', '31': 'S', '32': 'S', '33': 'R', '34': 'G', '35': 'S', '36': 'I', '37': 'R', '38': 'G', '39': 'E', '40': 'S', '41': 'E', '42': 'R', '43': 'R', '44': 'S', '45': '.', '46': 'E', '47': '.', '48': '.', '49': '.', '50': '.', '51': 'H', '52': '.', '53': 'S', '54': '.', '55': '.', '56': 'R', '57': '.', '58': 'G', '59': '.', '60': '.', '61': 'R', '62': '.', '63': '.', '64': '.', '65': '.', '66': 'B', '67': '.', '68': 'E', '69': '.', '70': '.', '71': 'G', '72': '.', '73': 'S', '74': '.', '75': 'B', '76': 'L', '77': 'X', '78': 'K', '79': 'I', '80': 'T', '81': 'O', '82': 'B', '83': 'S', '84': 'I', '85': 'O', '86': 'N', '87': 'T', '88': 'L', '89': 'N', '90': '.', '91': 'S', '92': '.', '93': '.', '94': 'E', '95': '.', '96': 'P', '97': '.', '98': 'R', '99': '.', '100': '.', '101': 'E', '102': '.', '103': 'R', '104': '.', '105': 'R', '106': 'P', '107': 'I', '108': 'O', '109': 'R', '110': 'P', '111': 'O', '112': 'G', '113': 'N', '114': 'B', '115': 'P', '116': 'O',
          '117': 'E', '118': 'S', '119': 'N', '120': '.', '121': 'R', '122': '.', '123': '.', '124': 'G', '125': '.', '126': 'C', '127': '.', '128': 'E', '129': '.', '130': '.', '131': 'G', '132': '.', '133': 'S', '134': '.', '135': '.', '136': 'G', '137': '.', '138': '.', '139': 'S', '140': '.', '141': 'I', '142': '.', '143': 'G', '144': '.', '145': '.', '146': 'S', '147': '.', '148': 'E', '149': '.', '150': '.', '151': 'S', '152': '.', '153': '.', '154': 'E', '155': '.', '156': 'V', '157': '.', '158': 'S', '159': '.', '160': '.', '161': 'E', '162': '.', '163': 'R', '164': '.', '165': 'S', '166': 'O', '167': 'R', '168': 'M', '169': 'V', '170': 'B', '171': 'S', '172': 'O', '173': 'T', '174': 'H', '175': 'N', '176': 'W', '177': 'P', '178': 'O', '179': 'L', '180': '.', '181': 'R', '182': '.', '183': '.', '184': 'E', '185': '.', '186': 'B', '187': '.', '188': 'R', '189': '.', '190': '.', '191': 'G', '192': '.', '193': 'E', '194': '.', '195': '.', '196': 'G', '197': '.', '198': '.', '199': 'S', '200': '.', '201': 'P', '202': '.', '203': 'G', '204': '.', '205': '.', '206': 'S', '207': '.', '208': 'S', '209': '.', '210': '.', '211': 'R', '212': '.', '213': '.', '214': 'E', '215': '.', '216': 'L', '217': '.', '218': 'R', '219': '.', '220': '.', '221': 'G', '222': '.', '223': 'G', '224': '.'}


class Scrabble():
    """Group of methods for scrabble game"""

    def __init__(self):
        self.trie = Trie()
        for word in scrabble_words:
            self.trie.add_word(word.lower())


    # def score_word(self):
        # pass

    def find_words(self, board, user_letters):
        """iterate through board letters and return list of possible words"""
        possible_words = {}
        unique_board_letters = set()
        # user_letters_and_board_letter = user_letters
        for key in board:
            if board[key] != '.':  # if there's a letter at that position in the board
                unique_board_letters.add(board[key].lower())
        for letter in unique_board_letters:
            user_letters_and_board_letter = user_letters + letter
            found_words_dict = self.trie.find_words(user_letters_and_board_letter)
            for word in found_words_dict:
                if word not in possible_words:
                    possible_words[word] = found_words_dict[word]

        return possible_words


scrabble = Scrabble()

start = datetime.now()
possible_words = scrabble.find_words(board, user_letters)
end = datetime.now()

print(f'Duration: {end - start}')
print(f'Len possible words: {len(possible_words)}')


start = datetime.now()
possible_words = scrabble.find_words(board2, user_letters)
end = datetime.now()

print(f'Duration: {end - start}')
print(f'Len possible words: {len(possible_words)}')
