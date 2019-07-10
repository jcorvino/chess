from game.pieces import King, Queen, Rook, Bishop, Knight, Pawn


class GameBoard:
    """
    Chess game board (8x8).

    Columns span from A to H. Rows span from 1 to 8.
    """

    initial_white_positions = {
        King: ('E1',),
        Queen: ('D1',),
        Rook: ('A1', 'H1',),
        Bishop: ('C1', 'F1',),
        Knight: ('B1', 'G1',),
        Pawn: (i + '2' for i in 'ABCDEFGH'),
    }

    initial_black_positions = {
        King: ('E8',),
        Queen: ('D8',),
        Rook: ('A8', 'H8',),
        Bishop: ('C8', 'F8',),
        Knight: ('B8', 'G8',),
        Pawn: (i + '7' for i in 'ABCDEFGH'),
    }

    def __init__(self):
        """
        Create starting game board
        """

        # List containing all active board pieces
        self.pieces = []

        # Populate white pieces on game board
        for piece_type, locations in self.initial_white_positions.items():
            for location in locations:
                self.pieces.append(piece_type('white', location))

        # Populate black pieces on game board
        for piece_type, locations in self.initial_black_positions.items():
            for location in locations:
                self.pieces.append(piece_type('black', location))
