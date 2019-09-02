from itertools import cycle

from .board import GameBoard
from .moves import GameMoves
from .player import Player


def create_player(color, default_name):
    """
    Create a chess player.

    :param color: player's color
    :param default_name: player's default name
    :return: Player object
    """
    name = input(f'\nWho will play as {color} [{default_name}]? ') or default_name
    return Player(name)


class Chess:
    """
    Main game logic
    """
    def __init__(self, board=None, player1=None, player2=None):
        self.board = board
        self.player1 = player1
        self.player2 = player2

        if self.board is None:  # create board if one is not provided
            self.board = GameBoard()

    def play(self):
        print('Let\'s play a game of chess!')
        if self.player1 is None:
            self.player1 = create_player('white', 'player 1')

        if self.player2 is None:
            self.player2 = create_player('black', 'player 2')

        players = cycle([self.player1, self.player2])
        player = next(players)
        invalid_msg = 'Invalid input. Type "exit" if you\'d like to quit. Type "help" if you\'d like instructions.\n'

        while True:
            print(f'It\'s {player.name}\'s turn. What would you like to do?')
            print(self.display())
            user_choice = input('').split()

            if len(user_choice) == 0:
                # no input
                print(invalid_msg)
                continue

            if user_choice[0].lower() == 'move':
                if len(user_choice) == 3:
                    print(self.move(user_choice[1], user_choice[2]))
            elif user_choice[0].lower() == 'get_moves':
                if len(user_choice) == 2:
                    print(self.get_moves(user_choice[1]))
            elif user_choice[0].lower() == 'exit':
                print('Goodbye.')
                return
            elif user_choice[0].lower() == 'help':
                print('Available functions:\nexit\nget_moves\nhelp\nmove')
            else:
                print(invalid_msg)
                continue

            player = next(players)

    def move(self, location, new_location):
        """
        Alias for GameMoves.move
        """
        return GameMoves.move(self.board, location, new_location)

    def get_moves(self, location):
        """
        Alias for GameMoves.get_moves
        """
        return GameMoves.get_moves(self.board, location)

    def display(self):
        """
        Current board layout
        """
        cols = GameBoard.cols
        rows = GameBoard.rows
        HLINE = '-+' * 9 + '-'  # horizontal line

        header = '|'.join(list(' ' + cols + ' '))

        def display_row(row):
            """
            String representation of a single row of the chess board.

            :param row: row number
            :return: chess board row
            """
            line_no = f'{row}'
            output = [line_no]
            for col in cols:
                piece = self.board[col + row]
                if piece is None:
                    output.append(' ')
                else:
                    output.append(piece.character)
            output.append(line_no)
            return '|'.join(output)

        output = [header]  # list of strings which will show the chess board
        for row in rows:
            output.append(HLINE)
            output.append(display_row(row))
        output.append(HLINE)
        output.append(header)

        return '\n'.join(output)

    def load_game(self, game):
        """
        Load an existing chess game
        """
        self.board = game.board
        self.player1 = game.player1
        self.player2 = game.player2
