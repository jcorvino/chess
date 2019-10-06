import unittest
from src.chess.board import GameBoard
from src.chess.pieces import King, Queen, Rook, Bishop, Knight, Pawn, GamePiece


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

    def test_initial_position(self):
        # Test GameBoard.__init__
        gb = GameBoard()

        # Check Pawns
        for col in GameBoard.cols:
            self.assertIsInstance(gb['%s2' % col], Pawn)
            self.assertIsInstance(gb['%s7' % col], Pawn)

        # Check Rooks
        self.assertIsInstance(gb['A1'], Rook)
        self.assertIsInstance(gb['H1'], Rook)
        self.assertIsInstance(gb['A8'], Rook)
        self.assertIsInstance(gb['H8'], Rook)

        # Check Knights
        self.assertIsInstance(gb['B1'], Knight)
        self.assertIsInstance(gb['G1'], Knight)
        self.assertIsInstance(gb['B8'], Knight)
        self.assertIsInstance(gb['G8'], Knight)

        # Check Bishops
        self.assertIsInstance(gb['C1'], Bishop)
        self.assertIsInstance(gb['F1'], Bishop)
        self.assertIsInstance(gb['C8'], Bishop)
        self.assertIsInstance(gb['F8'], Bishop)

        # Check Queens
        self.assertIsInstance(gb['D1'], Queen)
        self.assertIsInstance(gb['D8'], Queen)

        # Check Kings
        self.assertIsInstance(gb['E1'], King)
        self.assertIsInstance(gb['E8'], King)

