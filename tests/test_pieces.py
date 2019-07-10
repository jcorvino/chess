import unittest
from game import pieces


class TestPieces(unittest.TestCase):

    def test_base_class(self):
        # Incorrect initial location
        self.assertRaises(ValueError, pieces.GamePiece, name='king', color='white', location='somewhere')
        self.assertRaises(ValueError, pieces.GamePiece, name='king', color='white', location='A9')
        self.assertRaises(ValueError, pieces.GamePiece, name='king', color='white', location='I2')

        # Incorrect color
        self.assertRaises(ValueError, pieces.GamePiece, name='king', color='green', location='A1')

        # Incorrect name
        self.assertRaises(ValueError, pieces.GamePiece, name='wrong name', color='white', location='A1')

        # Verify has_moved property
        # No errors expected
        piece = pieces.GamePiece(name='king', color='black', location='H8')
        self.assertFalse(piece.has_moved)
        piece.location = 'A1'  # move piece
        self.assertTrue(piece.has_moved)

    def test_subclasses(self):
        # Verify name of each piece.
        # No Errors expected
        king = pieces.King(color='white', location='A1')
        self.assertEqual(king.name, 'king')

        queen = pieces.Queen(color='white', location='A1')
        self.assertEqual(queen.name, 'queen')

        rook = pieces.Rook(color='white', location='A1')
        self.assertEqual(rook.name, 'rook')

        bishop = pieces.Bishop(color='white', location='A1')
        self.assertEqual(bishop.name, 'bishop')

        knight = pieces.Knight(color='white', location='A1')
        self.assertEqual(knight.name, 'knight')

        pawn = pieces.Pawn(color='white', location='A1')
        self.assertEqual(pawn.name, 'pawn')
