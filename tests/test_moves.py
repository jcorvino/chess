import unittest
from src.chess.board import GameBoard
from src.chess.moves import GameMoves


class TestGameMoves(unittest.TestCase):
    """
    Test GameMoves class
    """
    def setUp(self):
        # Create initial chess board for tests
        self.gb = GameBoard()

    def test_pawn_attack_moves(self):
        # Test GameMoves._pawn_attack_moves
        location = 'A2'
        pawn = self.gb[location]
        attacks = GameMoves._pawn_attack_moves(self.gb, pawn, location)
        self.assertSetEqual(attacks, set())  # no attacks

        new_location = 'D6'
        self.gb[new_location] = pawn  # create new white pawn
        attacks = GameMoves._pawn_attack_moves(self.gb, pawn, new_location)
        self.assertSetEqual(attacks, set(['C7', 'E7']))  # 2 attacks
