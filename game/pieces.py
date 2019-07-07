from abc import ABC, abstractmethod
import re


class AbstractGamePiece(ABC):
    """
    Game piece class.

    Base class for all chess pieces.
    """

    def __init__(self, name, color, location):
        self._name = name
        self._color = color
        self._location = location
        self.has_moved = False

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        if val.lower() not in ['black', 'white']:
            raise ValueError('Game piece color must be black or white not \'%s\'' % val)
        self._color = val.lower()

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, val):
        if re.match('[A-H][1-8]', val) and val != self._location:
            self._location = val
            self.has_moved = True
        else:
            raise ValueError('Game piece moved to an invalid location: \'%s\'' % val)

    @property
    @abstractmethod
    def moves(self):
        pass  # TODO: Move "moves" functionality to separate module?


class King(AbstractGamePiece):
    """
    The King.
    """
    def __init__(self, color, location):
        super().__init__('king', color, location)

    def moves(self):
        return 'one'


if __name__ == '__main__':
    king = King('white', 'D1')
    print(king.color)
    print(king.name)
    print(king.moves)
    print(king.location)
