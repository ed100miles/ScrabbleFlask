from typing import Any, Dict, Union, List, Set, Tuple
from scrabbleWords import scrabble_words
from datetime import datetime
from collections import Counter


class Scrabble():
    """Facade providing public interface for implementation of scrabble game"""

    def __init__(self, valid_scrabble_words: dict) -> None:
        self._scoreWord = Scorer()
        self.check_fits = FitBoard()
        self._trie = Trie(valid_scrabble_words)
        self._word_finder = WordFinder(self._trie)

    def find_words(self, board: Dict[str, str], user_letters: str) -> Dict[Any, List[Tuple[str, str]]]:
        """Takes dict of letters on board and a string of users letters and return dict of possible words + definitions"""
        possible_words: Dict[str, str] = {}
        unique_board_letters: Set[str] = set()
        for key in board:
            if board[key] != '.':               # if there's a letter at that position in the board
                unique_board_letters.add(board[key].lower())

        if len(unique_board_letters) > 0:   # if there's any letters on the board
            for letter in unique_board_letters:     # check what words can be made w/ board+user letters
                user_letters_and_board_letter = user_letters + letter
                found_words_dict = self._word_finder.find_words(
                    user_letters_and_board_letter)
                for word in found_words_dict:
                    # check if word can fit on the board:
                    if self.check_fits.fits_board(board, word):
                        if word not in possible_words:
                            # add word to dict with definition as key
                            possible_words[word] = found_words_dict[word]
        else:                                                   # if there's no letters on the board
            possible_words = self._word_finder.find_words(
                user_letters)                                   # just return words user can make

        # add scores to words:
        possible_words_with_scores_and_defs = self._scoreWord._score_word_dict(
            possible_words)
        return possible_words_with_scores_and_defs


class Trie:
    """Create and populate Trie data structure."""

    class _Node:
        """Non-public Node subclass for Trie class"""

        def __init__(self, letter: str = None, is_word: Union[bool, str] = False) -> None:
            """Create Trie node instance"""
            self.letter = letter
            self.is_word = is_word
            self.children: Dict = {}

    def __init__(self, words_for_trie: Dict[str, str]) -> None:
        """Initialise Trie structure with words_to_add input"""
        self.root = self._Node()
        self.words_for_trie: Dict[str, str] = words_for_trie
        self.populate_trie(self.words_for_trie)

    def populate_trie(self, words_to_add) -> None:
        """Adds dict of words to Trie data structure."""
        for word in words_to_add:
            self.add_word(word.lower())

    def add_word(self, word: str) -> None:
        """Adds single word str to the Trie tree, with each letter as a _Node instance."""
        index_node = self.root
        is_word: Union[bool, str] = False
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


class WordFinder:
    """Collection of methods for finding valid words in a given a Trie instance"""

    def __init__(self, trie_instance) -> None:
        self._trie = trie_instance

    def find_words(self, user_letters: str) -> dict:
        """Returns dict of words in Trie with matching letters in user_letters string.
            Dict comprised of matching words as keys and definitions as values."""
        self.found_words: List[str] = []
        self._find_words(Counter(user_letters))

        # convert found words to dict and add definitions for values:
        found_words_and_defs = {}
        for word in self.found_words:
            word_up = word.upper()
            found_words_and_defs[word] = scrabble_words[word_up]
        return found_words_and_defs

    def _find_words(self, user_letters: Dict[str, int], node=None) -> None:
        """Private. Appends to self.found_words list all words added to Trie instance that can be made using user_letters"""
        if node == None:
            node = self._trie.root
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


class Scorer:
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

    def _score_word_dict(self, word_itter: Dict[str, str]) -> Dict[Any, List[Tuple[str, str]]]:
        """Returns dict with score as key and list of tuples (word, definition) as vaule. Takes dict of words:definitions as input."""
        words_defs_scores_dict = {}
        for word in word_itter:
            score = self._score_word(word)
            if score not in words_defs_scores_dict:
                words_defs_scores_dict[score] = [(word, word_itter[word])]
            else:
                words_defs_scores_dict[score].append((word, word_itter[word]))
        return words_defs_scores_dict


class FitBoard:
    """Component class providing methods that confirm if a word fits on a given board"""

    def fits_board(self, board: dict, word: str) -> bool:
        """Returns True if word fits either horizontally or vertically on a board and doesn't clash with other letters, else return False. """
        # Start by creating empty 2d array board representation:
        out_board: List = [[None] * 15 for i in range(15)]
        # edit board to reflect input:
        for x in board.items():
            key, value = x
            y, z = int(key) // 15, int(key) % 15
            out_board[y][z] = value
        fits_horizontal = self._check_horizontal(word, out_board)
        # rotatate the board 270 degrees to check if word fits vertically:
        for _ in range(3):
            out_board = list(zip(*out_board[::-1]))
        fits_vertical = self._check_horizontal(word, out_board)
        return fits_horizontal or fits_vertical

    def _check_horizontal(self, word: str, out_board: List) -> bool:
        """Iterates through word and board calling fits_left_right method. 
        Returns True if there's a position where the word fits horizontally on the board, else False."""
        for letter_num, letter in enumerate(word):
            for row in out_board:
                for square_num, square in enumerate(row):
                    if letter == square.lower():
                        space_left, space_right = self._fits_left_right(
                            word, letter_num, letter, row, square_num, square)
                        if space_left and space_right:
                            return True
        return False

    # Private methods:

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
            if square == '.' or square == letter:
                after_space_available += 1
            else:  #  if not consecutive '.'s break
                break
        if after_space_needed <= after_space_available:
            enough_space_right = True
        # check sufficient space before letter:
        before_space_available = 0
        for square in reversed(row[:square_num]):
            if square == '.' or square == letter:
                before_space_available += 1
            else:
                break  #  if not consecutive '.'s break
        if before_space_needed <= before_space_available:
            enough_space_left = True
        return (enough_space_left, enough_space_right)


scrabble = Scrabble(valid_scrabble_words=scrabble_words)

if __name__ == "__main__":
    print(f'{__file__} running as __main__')

# TODO: Write some proper unit tests:

    # Quick tests setup:
    fits = FitBoard()
    user_letters = 'arbon'
    board = {str(key): '.' for key in range(225)}
    board['2'] = 'C'

    # find words tests:
    assert list(scrabble.find_words(board, user_letters).keys()) == [
        7, 6, 5, 9, 8, 10]

    # fits board tests:
    assert fits.fits_board(board, 'cat') == True
    board['224'] = 'B'
    assert fits.fits_board(board, 'bat') == False

    print('Tests sucessfull')

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
