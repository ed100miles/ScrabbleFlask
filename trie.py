from playground import fits_left_right
from scrabbleWords import scrabble_words
from datetime import datetime


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
        self.found_words = []   # create or clear a list for matching words
        user_letters_dict = {}  # create dict of user letters e.g {'a':3}
        for letter in user_letters:
            if letter not in user_letters_dict:
                user_letters_dict[letter] = 1
            else:
                user_letters_dict[letter] += 1
        self._find_words(user_letters_dict)
        # convert found words to dict and add definitions for values:
        found_words_and_defs = {}
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


class Scrabble():
    """Composite class providing public interface for implementation of scrabble game"""

    def __init__(self):
        self._trie = Trie()
        self._scoreWord = ScoreWord()  # non-pub instance of ScoreWord class
        self.check_fits = FitsBoard()
        for word in scrabble_words:
            self._trie.add_word(word.lower())

    def find_words(self, board: dict, user_letters: str):
        """Takes dict of letters on board and string of users letters and return dict of possible words + definitions"""
        possible_words = {}
        unique_board_letters = set()
        for key in board:
            if board[key] != '.':               # if there's a letter at that position in the board
                unique_board_letters.add(board[key].lower())

        if len(unique_board_letters) > 0:   # if there's any letters on the board
            for letter in unique_board_letters:     # check what words can be made
                user_letters_and_board_letter = user_letters + letter
                found_words_dict = self._trie.find_words(
                    user_letters_and_board_letter)
                for word in found_words_dict:
                    # if word can fit on the board
                    if self.check_fits.fits_board(board, word):
                        if word not in possible_words:
                            # add word to dict with definition as key
                            possible_words[word] = found_words_dict[word]
        else:                                                   # if there's no letters on the board
            possible_words = self._trie.find_words(
                user_letters)                                   # just return words user can make

        #  Here we want to take possible words and see if they fit the board?

        possible_words_with_scores_and_defs = self._scoreWord._score_word_dict(
            possible_words)
        return possible_words_with_scores_and_defs


class ScoreWord:
    """Component class providing methods to add scores to words"""

    def _score_word(self, word: str):
        """Returns scrabble score of word string"""
        _score = 0
        _letter_scores = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1,
                          'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 8, 'w': 4, 'x': 8, 'y': 4, 'z': 10}
        _score_word = word.lower()  # just incase casing is wrong
        for letter in _score_word:
            _score += _letter_scores[letter]
        return _score

    def _score_word_dict(self, word_dict: dict):
        """Returns dict with score as key and list of tuples (word, definition) as vaule. Takes dict of words:definitions as input."""
        words_defs_scores_dict = {}
        for word in word_dict:
            score = self._score_word(word)
            if score not in words_defs_scores_dict:
                words_defs_scores_dict[score] = [(word, word_dict[word])]
            else:
                words_defs_scores_dict[score].append((word, word_dict[word]))
        return words_defs_scores_dict


class FitsBoard:
    """Component class providing methods that confirm if a word fits on a given board"""

    def _check_horizontal(self, word, out_board):
        """Iterates through word and board running fits_left_right method. 
        Returns True if there's a position where the word fits horizontally on board."""
        for letter_num, letter in enumerate(word):
            for row in out_board:
                for square_num, square in enumerate(row):
                    if letter == square.lower():
                        space_left, space_right = self._fits_left_right(
                            word, letter_num, letter, row, square_num, square)
                        # return true if space to left and right!
                        if space_left and space_right:
                            return True
        return False

    def _fits_left_right(self, word, letter_num, letter, row, square_num, square):
        """Returns tuple (True, True) if a word fits horizontally at a given position on a board."""
        enough_space_right = False
        enough_space_left = False

        # calculate space required before and after letter for word to fit
        before_space_needed = word.index(letter, letter_num)

        if square_num != '0':
            #  +1 to ensure there's space before any letters if not on left edge of board
            before_space_needed + 1

        after_space_needed = len(
            word) - word.index(letter, letter_num)
        # no space needed to right if last letter of word is on right edge of the board
        # square_num == 14 and letter is word[-1] or
        if square_num + after_space_needed == 15:
            after_space_needed -= 1

        # check sufficient space after letter:
        after_space_available = 0
        for square in row[square_num+1:]:
            if square == '.':
                after_space_available += 1
            else:  #  if not consecutive '.'s break
                break
        if after_space_needed <= after_space_available:
            enough_space_right = True

        # check sufficient space before letter:
        before_space_available = 0
        for square in reversed(row[:square_num]):
            if square == '.':
                before_space_available += 1
            else:
                break  #  if not consecutive '.'s break
        if before_space_needed <= before_space_available:
            enough_space_left = True

        return (enough_space_left, enough_space_right)

    def fits_board(self, board, word):
        """Returns True if word fits either horizontally or vertically on a board and doesn't clash with other letters, else return False. """
        # Start by creating empty 2d array board representation:
        out_board = [[None] * 15 for i in range(15)]

        # edit board to reflect input:
        for x in board.items():
            key, value = x
            y = int(key) // 15
            z = int(key) % 15
            out_board[y][z] = value

        fits_horizontal = self._check_horizontal(word, out_board)

        # rotatate the board 270 degrees to check if word fits vertically:
        for _ in range(3):
            out_board = list(zip(*out_board[::-1]))

        fits_vertical = self._check_horizontal(word, out_board)

        return fits_horizontal or fits_vertical


scrabble = Scrabble()

# user_letters = 'cat'
# board = {'0': '.', '1': '.', '2': '.', '3': '.', '4': '.', '5': '.', '6': '.', '7': '.', '8': '.', '9': '.', '10': '.', '11': '.', '12': '.', '13': '.', '14': '.', '15': '.', '16': '.', '17': '.', '18': '.', '19': '.', '20': '.', '21': '.', '22': '.', '23': '.', '24': '.', '25': '.', '26': '.', '27': '.', '28': '.', '29': '.', '30': '.', '31': '.', '32': '.', '33': '.', '34': '.', '35': '.', '36': '.', '37': '.', '38': '.', '39': '.', '40': '.', '41': '.', '42': '.', '43': '.', '44': '.', '45': '.', '46': '.', '47': '.', '48': '.', '49': '.', '50': '.', '51': '.', '52': '.', '53': '.', '54': '.', '55': '.', '56': '.', '57': '.', '58': '.', '59': '.', '60': '.', '61': '.', '62': '.', '63': '.', '64': '.', '65': '.', '66': '.', '67': '.', '68': '.', '69': '.', '70': '.', '71': '.', '72': '.', '73': '.', '74': '.', '75': '.', '76': '.', '77': '.', '78': '.', '79': '.', '80': '.', '81': '.', '82': '.', '83': '.', '84': '.', '85': '.', '86': '.', '87': '.', '88': '.', '89': '.', '90': '.', '91': '.', '92': '.', '93': '.', '94': '.', '95': '.', '96': '.', '97': '.', '98': '.', '99': '.', '100': '.', '101': '.', '102': '.', '103': '.', '104': '.', '105': '.', '106': '.', '107': '.', '108': '.', '109': '.', '110': '.', '111': '.', '112': '.', '113': '.', '114': '.', '115': '.', '116': '.',
#          '117': '.', '118': '.', '119': '.', '120': '.', '121': '.', '122': '.', '123': '.', '124': '.', '125': '.', '126': '.', '127': '.', '128': '.', '129': '.', '130': '.', '131': '.', '132': '.', '133': '.', '134': '.', '135': '.', '136': '.', '137': '.', '138': '.', '139': '.', '140': '.', '141': '.', '142': '.', '143': '.', '144': '.', '145': '.', '146': '.', '147': '.', '148': '.', '149': '.', '150': '.', '151': '.', '152': '.', '153': '.', '154': '.', '155': '.', '156': '.', '157': '.', '158': '.', '159': '.', '160': '.', '161': '.', '162': '.', '163': '.', '164': '.', '165': '.', '166': '.', '167': '.', '168': '.', '169': '.', '170': '.', '171': '.', '172': '.', '173': '.', '174': '.', '175': '.', '176': '.', '177': '.', '178': '.', '179': '.', '180': '.', '181': '.', '182': '.', '183': '.', '184': '.', '185': '.', '186': '.', '187': '.', '188': '.', '189': '.', '190': '.', '191': '.', '192': '.', '193': '.', '194': '.', '195': '.', '196': '.', '197': '.', '198': '.', '199': '.', '200': '.', '201': '.', '202': '.', '203': '.', '204': '.', '205': '.', '206': '.', '207': '.', '208': '.', '209': '.', '210': '.', '211': '.', '212': '.', '213': '.', '214': '.', '215': '.', '216': '.', '217': '.', '218': '.', '219': '.', '220': '.', '221': '.', '222': '.', '223': '.', '224': '.'}
# board2 = {'0': '.', '1': '.', '2': '.', '3': 'E', '4': 'R', '5': 'G', '6': 'V', '7': 'E', '8': 'R', '9': 'G', '10': '.', '11': '.', '12': '.', '13': 'S', '14': '.', '15': '.', '16': '.', '17': '.', '18': '.', '19': '.', '20': '.', '21': 'O', '22': '.', '23': '.', '24': '.', '25': '.', '26': 'S', '27': '.', '28': 'E', '29': '.', '30': '.', '31': 'S', '32': 'S', '33': 'R', '34': 'G', '35': 'S', '36': 'I', '37': 'R', '38': 'G', '39': 'E', '40': 'S', '41': 'E', '42': 'R', '43': 'R', '44': 'S', '45': '.', '46': 'E', '47': '.', '48': '.', '49': '.', '50': '.', '51': 'H', '52': '.', '53': 'S', '54': '.', '55': '.', '56': 'R', '57': '.', '58': 'G', '59': '.', '60': '.', '61': 'R', '62': '.', '63': '.', '64': '.', '65': '.', '66': 'B', '67': '.', '68': 'E', '69': '.', '70': '.', '71': 'G', '72': '.', '73': 'S', '74': '.', '75': 'B', '76': 'L', '77': 'X', '78': 'K', '79': 'I', '80': 'T', '81': 'O', '82': 'B', '83': 'S', '84': 'I', '85': 'O', '86': 'N', '87': 'T', '88': 'L', '89': 'N', '90': '.', '91': 'S', '92': '.', '93': '.', '94': 'E', '95': '.', '96': 'P', '97': '.', '98': 'R', '99': '.', '100': '.', '101': 'E', '102': '.', '103': 'R', '104': '.', '105': 'R', '106': 'P', '107': 'I', '108': 'O', '109': 'R', '110': 'P', '111': 'O', '112': 'G', '113': 'N', '114': 'B', '115': 'P', '116': 'O',
#   '117': 'E', '118': 'S', '119': 'N', '120': '.', '121': 'R', '122': '.', '123': '.', '124': 'G', '125': '.', '126': 'C', '127': '.', '128': 'E', '129': '.', '130': '.', '131': 'G', '132': '.', '133': 'S', '134': '.', '135': '.', '136': 'G', '137': '.', '138': '.', '139': 'S', '140': '.', '141': 'I', '142': '.', '143': 'G', '144': '.', '145': '.', '146': 'S', '147': '.', '148': 'E', '149': '.', '150': '.', '151': 'S', '152': '.', '153': '.', '154': 'E', '155': '.', '156': 'V', '157': '.', '158': 'S', '159': '.', '160': '.', '161': 'E', '162': '.', '163': 'R', '164': '.', '165': 'S', '166': 'O', '167': 'R', '168': 'M', '169': 'V', '170': 'B', '171': 'S', '172': 'O', '173': 'T', '174': 'H', '175': 'N', '176': 'W', '177': 'P', '178': 'O', '179': 'L', '180': '.', '181': 'R', '182': '.', '183': '.', '184': 'E', '185': '.', '186': 'B', '187': '.', '188': 'R', '189': '.', '190': '.', '191': 'G', '192': '.', '193': 'E', '194': '.', '195': '.', '196': 'G', '197': '.', '198': '.', '199': 'S', '200': '.', '201': 'P', '202': '.', '203': 'G', '204': '.', '205': '.', '206': 'S', '207': '.', '208': 'S', '209': '.', '210': '.', '211': 'R', '212': '.', '213': '.', '214': 'E', '215': '.', '216': 'L', '217': '.', '218': 'R', '219': '.', '220': '.', '221': 'G', '222': '.', '223': 'G', '224': '.'}
#

# fits = FitsBoard()
# start = datetime.now()
# print(fits.fits_board(board, 'cat'))
# print(f'Duration: {datetime.now() - start}')


# print(scrabble.find_words(board2, user_letters))

# start = datetime.now()
# possible_words = scrabble.find_words(board, user_letters)
# end = datetime.now()

# print(f'Duration: {end - start}')
# print(f'Len possible words: {len(possible_words)}')


# start = datetime.now()
# possible_words = scrabble.find_words(board2, user_letters)
# end = datetime.now()

# print(f'Duration: {end - start}')
# print(f'Len possible words: {len(possible_words)}')
