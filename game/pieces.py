import re


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

    def __init__(self, name, color, location):
        self._name = None
        self._color = None
        self._location = None

        self.name = name
        self.color = color
        self.location = location
        self.has_moved = False

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

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, val):
        if re.match('[A-H][1-8]', val) and val != self._location:
            self._location = val
            self.has_moved = True
        else:
            raise ValueError('Game piece moved to an invalid location: \'%s\'' % str(val))


class King(GamePiece):
    def __init__(self, color, location):
        super().__init__('king', color, location)


class Queen(GamePiece):
    def __init__(self, color, location):
        super().__init__('queen', color, location)


class Rook(GamePiece):
    def __init__(self, color, location):
        super().__init__('rook', color, location)


class Bishop(GamePiece):
    def __init__(self, color, location):
        super().__init__('bishop', color, location)


class Knight(GamePiece):
    def __init__(self, color, location):
        super().__init__('knight', color, location)


class Pawn(GamePiece):
    def __init__(self, color, location):
        super().__init__('pawn', color, location)
