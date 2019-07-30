import re
from pieces import King, Queen, Rook, Bishop, Knight, Pawn


class BoardDict(dict):
	"""
	Special dictionary that represents a chess game board
	"""
	def __init__(self):
		"""
		Auto load the keys for the game board (A1-H8)
		"""
		rows = 'ABCDEFGH'
		cols = '12345678'
		d = dict()
		for row in rows:
			for col in cols:
				d[row + col] = None
		super().__init__(d)
	
	def __setitem__(self, key, value):
		"""
		Prevent user from modifying keys
		"""
		if not re.match('[A-H][1-8]', key):
			raise KeyError(f'Board can only have positions A1-H8, not {key}')
		super().__setitem__(key, value)


class GameBoard:
	"""
	Chess game board (8x8).

	Columns span from A to H. Rows span from 1 to 8.
	"""
	_rows = 'ABCDEFGH'
	_cols = '12345678'
	
	initial_white_positions = {
		King: ('E1',),
		Queen: ('D1',),
		Rook: ('A1', 'H1',),
		Bishop: ('C1', 'F1',),
		Knight: ('B1', 'G1',),
		Pawn: (i + '2' for i in _rows),
	}

	initial_black_positions = {
		King: ('E8',),
		Queen: ('D8',),
		Rook: ('A8', 'H8',),
		Bishop: ('C8', 'F8',),
		Knight: ('B8', 'G8',),
		Pawn: (i + '7' for i in _rows),
	}

	def __init__(self):
		"""
		Create starting game board
		"""
		self.board = BoardDict()  # empty board
		self.history = list()  # list of all past moves

		# Populate white pieces on game board
		for piece_type, locations in self.initial_white_positions.items():
			for location in locations:
				self.board[location] = piece_type('white')

		# Populate black pieces on game board
		for piece_type, locations in self.initial_black_positions.items():
			for location in locations:
				self.board[location] = piece_type('black')

	def get_moves(location):
		"""
		Gets the allowed moves for a piece in the specified location
		"""
		pass


if __name__ == '__main__':
	print('test')
	mygb = GameBoard()
	print(mygb.board)