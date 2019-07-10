from game.board import GameBoard


class Chess:
    """
    Main game logic
    """
    def __init__(self):
        self.board = GameBoard()

    def play(self):
        print('Let\'s play a game of chess!')
        print(list(map(lambda x: (x.color + '-' + x.name, x.location), self.board.pieces)))
