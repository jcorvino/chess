import re
from copy import deepcopy
from game.pieces import King, Queen, Rook, Bishop, Knight, Pawn


class GameBoard(dict):
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

    default_options = {
        'turn': 'white',  # starting turn
        'history': list(),  # starting history
        'en_passant': None,  # possible en-passant attacks
    }

    def __init__(self, **user_options):
        """
        Create starting game board
        """
        default_options = deepcopy(self.default_options)  # ensure self.default_options is not modified

        # Update default_options with new values from user_options
        # Ignore user_option keys that do not appear in default_options
        # See https://stackoverflow.com/questions/14941115/update-dict-without-adding-new-keys
        default_options.update((key, user_options[key]) for key in default_options.keys() & user_options.keys())

        for key, value in default_options.items():
            setattr(self, key, value)

        # create dict with empty board positions
        d = {col + row: None for row in self.rows for col in self.cols}

        # Populate pieces on the game board
        for color in self.initial_positions.keys():
            for piece_type, locations in self.initial_positions[color].items():
                for location in locations:
                    d[location] = piece_type(color)

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


if __name__ == '__main__':
    mygb = GameBoard()
    print(mygb)
