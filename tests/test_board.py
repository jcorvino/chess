import unittest
from game.board import BoardDict, GameBoard


class TestBoard(unittest.TestCase):
    """
    Test board module
    """

    def test_board_dict(self):
        # Test BoardDict class
        board = BoardDict()

        # Incorrect location
        self.assertRaises(KeyError, board.__setitem__, 'I1', None)
        self.assertRaises(KeyError, board.__getitem__, 'A9')

    def test_game_board(self):
        # Test GameBoard
        pass
