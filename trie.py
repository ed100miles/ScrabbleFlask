from typing import Any, Dict, Union, List
from scrabbleWords import scrabble_words
from datetime import datetime
from collections import Counter

class Trie:
    """Create and populate Trie data structure and find words that can be made with given letters."""

    class _Node:
        """Non-public Node subclass for Trie class"""

        def __init__(self, letter: str = None, is_word:Union[bool, str] = False) -> None:
            """Create Trie node instance"""
            self.letter = letter
            self.is_word = is_word
            self.children: Dict  = {}

    def __init__(self) -> None:
        """Initialise instance of Trie class and set root"""
        self.root = self._Node()

    def add_word(self, word: str) -> None:
        """Adds word string to the Trie tree"""
        index_node = self.root
        is_word:Union[bool,str] = False
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

    def find_words(self, user_letters: str) -> dict:
        """Returns dict of words in Trie with matching letters in user_letters string.
            Dict comprised of matching words as keys and definitions as values."""
        self.found_words:List[str] = []   # create or clear a list for matching words
        self._find_words(Counter(user_letters))

        # convert found words to dict and add definitions for values:
        found_words_and_defs = {}
        for word in self.found_words:
            word_up = word.upper()
            found_words_and_defs[word] = scrabble_words[word_up]
        return found_words_and_defs

    # --- Private methods:

    def _find_words(self, user_letters:Dict[str,int], node=None) -> None:
        """Appends to self.found_words list all words added to Trie instance that can be made using user_letters"""
        if node == None:
            node = self.root
        if node.is_word:
            self.found_words.append(node.is_word)
        # Base case:
        if len(node.children) == 0 or sum(user_letters.values()) == 0:
            return None
        # else recur down each node.child where node.child in user_letters and count > 0
        for child in node.children:
            if child in user_letters and user_letters[child] > 0:
                user_letters_less_child = user_letters.copy()
                user_letters_less_child[child] -= 1
                self._find_words(user_letters_less_child, node.children[child])


class Scrabble():
    """Composite/Facade class providing public interface for implementation of scrabble game"""

    def __init__(self, scrabble_words:dict) -> None:
        self._scoreWord = ScoreWord() 
        self.check_fits = FitsBoard()
        self._trie = Trie()
        for word in scrabble_words:
            self._trie.add_word(word.lower())

    def find_words(self, board: dict, user_letters: str) -> dict:
        """Takes dict of letters on board and string of users letters and return dict of possible words + definitions"""
        possible_words = {}
        unique_board_letters = set()
        for key in board:
            if board[key] != '.':               # if there's a letter at that position in the board
                unique_board_letters.add(board[key].lower())

        if len(unique_board_letters) > 0:   # if there's any letters on the board
            for letter in unique_board_letters:     # check what words can be made w/ board+user letters
                user_letters_and_board_letter = user_letters + letter
                found_words_dict = self._trie.find_words(
                    user_letters_and_board_letter)
                for word in found_words_dict:
                    # check if word can fit on the board:
                    if self.check_fits.fits_board(board, word):
                        if word not in possible_words:
                            # add word to dict with definition as key
                            possible_words[word] = found_words_dict[word]
        else:                                                   # if there's no letters on the board
            possible_words = self._trie.find_words(
                user_letters)                                   # just return words user can make

        # add scores to words: 
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
        _word_to_score = word.lower()  # handle if casing is wrong
        for letter in _word_to_score:
            _score += _letter_scores[letter]
        return _score

    def _score_word_dict(self, word_itter: dict):
        """Returns dict with score as key and list of tuples (word, definition) as vaule. Takes dict of words:definitions as input."""
        words_defs_scores_dict = {}
        for word in word_itter:
            score = self._score_word(word)
            if score not in words_defs_scores_dict:
                words_defs_scores_dict[score] = [(word, word_itter[word])]
            else:
                words_defs_scores_dict[score].append((word, word_itter[word]))
        return words_defs_scores_dict


class FitsBoard:
    """Component class providing methods that confirm if a word fits on a given board"""

    def _check_horizontal(self, word: str, out_board: List) -> bool:
        """Iterates through word and board calling fits_left_right method. 
        Returns True if there's a position where the word fits horizontally on the board, else False."""
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

    def _fits_left_right(self, word: str, letter_num: int, letter: str,
                         row: List, square_num: int, square: str) -> tuple:
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

    def fits_board(self, board: dict, word: str) -> bool:
        """Returns True if word fits either horizontally or vertically on a board and doesn't clash with other letters, else return False. """
        # Start by creating empty 2d array board representation:
        out_board:List = [[None] * 15 for i in range(15)]
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


scrabble = Scrabble(scrabble_words=scrabble_words)


if __name__ == "__main__":
    print('I\'m your main man')

# TODO: Write some proper unit tests:

    user_letters = 'cat'
    board = {str(key):'.' for key in range(225)}
    board['2'] = 'C'

    fits = FitsBoard()
    start = datetime.now()
    print(fits.fits_board(board, 'cat'))
    print(f'Duration: {datetime.now() - start}')




# print(board)

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
