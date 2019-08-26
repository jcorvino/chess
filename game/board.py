import re
from game.pieces import King, Queen, Rook, Bishop, Knight, Pawn


class BoardDict(dict):
    """
    Special dictionary that represents a chess game board
    """
    def __init__(self):
        """
        Auto load the keys for the game board (A1-H8)
        """
        cols = 'ABCDEFGH'
        rows = '12345678'
        d = dict()
        for row in cols:
            for col in rows:
                d[row + col] = None
        super().__init__(d)

    def __setitem__(self, key, value):
        """
        Prevent user from modifying keys
        """
        if not re.match('[A-H][1-8]', key):
            raise KeyError(f'Invalid chess board position: {key}')
        super().__setitem__(key, value)

    def __getitem__(self, item):
        """
        Prevent user from accessing locations off the game board
        """
        if not re.match('[A-H][1-8]', item):
            raise KeyError(f'Invalid chess board position: {item}')
        return super().__getitem__(item)


class GameBoard:
    """
    Chess game board (8x8).

    Columns span from A to H. Rows span from 1 to 8.
    """
    cols = 'ABCDEFGH'
    rows = '12345678'

    initial_positions = {
        'white': {
            King: ('E1',),
            Queen: ('D1',),
            Rook: ('A1', 'H1',),
            Bishop: ('C1', 'F1',),
            Knight: ('B1', 'G1',),
            Pawn: (i + '2' for i in cols),
        },
        'black': {
            King: ('E8',),
            Queen: ('D8',),
            Rook: ('A8', 'H8',),
            Bishop: ('C8', 'F8',),
            Knight: ('B8', 'G8',),
            Pawn: (i + '7' for i in cols),
        }
    }

    def __init__(self, turn='white'):
        """
        Create starting game board
        """
        self.board = BoardDict()  # empty board
        self.history = list()  # list of all past moves
        self.turn = turn
        self.en_passant = None  # location of possible en passant attack.

        # Populate pieces on the game board
        for color in self.initial_positions.keys():
            for piece_type, locations in self.initial_positions[color].items():
                for location in locations:
                    self.board[location] = piece_type(color)


if __name__ == '__main__':
    mygb = GameBoard()
    print(mygb.board)
