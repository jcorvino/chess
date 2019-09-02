class GamePiece:
    """
    Game piece class.

    Base class for all chess pieces.
    """
    names = (
        'king',
        'queen',
        'rook',
        'bishop',
        'knight',
        'pawn',
    )

    colors = (
        'black',
        'white',
    )

    def __init__(self, name, color, has_moved=False):
        self._name = None
        self._color = None

        self.name = name
        self.color = color
        self.has_moved = has_moved

    def __repr__(self):
        if self.has_moved:
            arguments = f'\'{self.color}\', has_moved={self.has_moved}'
        else:
            arguments = f'\'{self.color}\''
        return type(self).__name__ + f'({arguments})'

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if val not in self.names:
            raise ValueError('Invalid game piece name: \'%s\'' % val)
        self._name = val

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        if val not in self.colors:
            raise ValueError('Game piece color must be black or white not \'%s\'' % val)
        self._color = val


class King(GamePiece):
    def __init__(self, *args, **kwargs):
        self.character = 'K'
        super().__init__('king', *args, **kwargs)


class Queen(GamePiece):
    def __init__(self, *args, **kwargs):
        self.character = 'Q'
        super().__init__('queen', *args, **kwargs)


class Rook(GamePiece):
    def __init__(self, *args, **kwargs):
        self.character = 'R'
        super().__init__('rook', *args, **kwargs)


class Bishop(GamePiece):
    def __init__(self, *args, **kwargs):
        self.character = 'B'
        super().__init__('bishop', *args, **kwargs)


class Knight(GamePiece):
    def __init__(self, *args, **kwargs):
        self.character = 'N'
        super().__init__('knight', *args, **kwargs)


class Pawn(GamePiece):
    def __init__(self, *args, **kwargs):
        self.character = 'P'
        super().__init__('pawn', *args, **kwargs)
