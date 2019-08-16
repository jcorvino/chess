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

    def __init__(self, name, color):
        self._name = None
        self._color = None

        self.name = name
        self.color = color
        self.has_moved = False

    def __repr__(self):
        return type(self).__name__ + '(\'' + str(self.color) + '\')'

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if val not in self.names:
            raise ValueError('Invalid game piece name: \'%s\'' % str(val))
        self._name = val

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        if val not in self.colors:
            raise ValueError('Game piece color must be black or white not \'%s\'' % str(val))
        self._color = val


class King(GamePiece):
    def __init__(self, color):
        super().__init__('king', color)


class Queen(GamePiece):
    def __init__(self, color):
        super().__init__('queen', color)


class Rook(GamePiece):
    def __init__(self, color):
        super().__init__('rook', color)


class Bishop(GamePiece):
    def __init__(self, color):
        super().__init__('bishop', color)


class Knight(GamePiece):
    def __init__(self, color):
        super().__init__('knight', color)


class Pawn(GamePiece):
    def __init__(self, color):
        super().__init__('pawn', color)
