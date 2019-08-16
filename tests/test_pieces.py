import unittest
from game import pieces


class TestPieces(unittest.TestCase):
    """
    Test cases for pieces module
    """

    def test_base_class(self):
        # Incorrect color
        self.assertRaises(ValueError, pieces.GamePiece, name='king', color='green')

        # Incorrect name
        self.assertRaises(ValueError, pieces.GamePiece, name='wrong name', color='white')

        # Verify has_moved property
        # No errors expected
        piece = pieces.GamePiece(name='king', color='black')
        self.assertFalse(piece.has_moved)

    def test_subclasses(self):
        # Verify name of each piece.
        # No Errors expected
        king = pieces.King(color='white')
        self.assertEqual(king.name, 'king')

        queen = pieces.Queen(color='white')
        self.assertEqual(queen.name, 'queen')

        rook = pieces.Rook(color='white')
        self.assertEqual(rook.name, 'rook')

        bishop = pieces.Bishop(color='white')
        self.assertEqual(bishop.name, 'bishop')

        knight = pieces.Knight(color='white')
        self.assertEqual(knight.name, 'knight')

        pawn = pieces.Pawn(color='white')
        self.assertEqual(pawn.name, 'pawn')
