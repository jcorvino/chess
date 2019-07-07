#TODO: Move to "chess" module


class Moves:
    """
    Class to hold all common and special chess moves.

    Move Descriptions:
    one-any: one step in any direction
    one-forward: one step forward
    diagonal: any number of steps diagonally
    straight: any number of steps vertically/horizontally
    jump: L shaped move (2 forward, 1 perpendicular). NOTE: "jump" can move over opponents unlike all other moves.
    castle: king and rook switch positions
    en-passant: special pawn attack
    pawn-attack: normal pawn attack (1 step forward-diagonal)
    """
    moves = {
            'king': ['one-any', 'castle'],
            'pawn': ['one-forward', 'pawn-attack', 'en-passant'],
            'bishop': ['diagonal'],
            'rook': ['straight', 'castle'],
            'knight': ['jump'],
            'queen': ['diagonal', 'straight'],
        }


if __name__ == '__main__':
    print(Moves.moves)
    Moves.moves = 'junk'
    print(Moves.moves)
