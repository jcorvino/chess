import sys
from .cli import Chess

if __name__ == '__main__':
    game = Chess()
    sys.exit(game.play())
