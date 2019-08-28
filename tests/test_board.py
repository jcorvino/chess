import unittest
from src.chess.board import GameBoard


class TestGameBoard(unittest.TestCase):
    """
    Test GameBoard class
    """
    def test_setitem(self):
        # Test GameBoard.__setitem__
        gb = GameBoard()

        # Incorrect location
        self.assertRaises(KeyError, gb.__setitem__, 'I1', None)
        self.assertRaises(KeyError, gb.__setitem__, 'a1', None)

        # Correct locations (no error)
        gb.__setitem__('A1', None)
        gb.__setitem__('H8', None)

    def test_getitem(self):
        # Test GameBoard.__getitem__
        gb = GameBoard()

        # Incorrect locations
        self.assertRaises(KeyError, gb.__getitem__, 'A9')
        self.assertRaises(KeyError, gb.__getitem__, 'A0')
        self.assertRaises(KeyError, gb.__getitem__, '00')
        self.assertRaises(KeyError, gb.__getitem__, 'aa')
        self.assertRaises(KeyError, gb.__getitem__, 'a9')
        self.assertRaises(KeyError, gb.__getitem__, 'A11')
        self.assertRaises(KeyError, gb.__getitem__, 'BB')

        # Correct locations (no error)
        gb.__getitem__('A1')
        gb.__getitem__('H8')

    def test_init(self):
        # Test GameBoard.__init__
        gb = GameBoard()
        gb2 = GameBoard(turn='black', en_passant='A3', history=['White pawn moved from A2 to A4'], invalid='abc')

        # Check turn, history, en_passant for gb
        self.assertEqual(gb.turn, 'white')
        self.assertListEqual(gb.history, [])
        self.assertIsNone(gb.en_passant)

        # Check turn, history, en_passant for gb2
        self.assertEqual(gb2.turn, 'black')
        self.assertListEqual(gb2.history, ['White pawn moved from A2 to A4'])
        self.assertEqual(gb2.en_passant, 'A3')
        self.assertRaises(AttributeError, getattr, gb2, 'invalid')  # invalid user_options should not be saved

