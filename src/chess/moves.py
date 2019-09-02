from .pieces import King, Queen, Rook, Bishop, Knight, Pawn


class GameMoves:
    """
    Class to determine which moves are allowed and to move pieces.
    """

    @staticmethod
    def move(board, location, new_location):
        """
        Move a piece on the board from location to new_location
        """
        # convert to upper case if user forgot
        new_location = new_location.upper()
        location = location.upper()

        # check if valid game piece
        piece = board[location]
        if piece is None:
            raise ValueError(f'No piece at {location}')

        # check if correct color
        if piece.color != board.turn:
            raise ValueError(f'Cannot move piece at {location}! It is not {piece.color}\'s turn')

        # check allowed moves
        valid_moves = GameMoves.get_moves(board, location)
        if new_location not in valid_moves:
            raise ValueError(f'Moving {piece.name} to {new_location} is not a valid move. Check get_moves function.')

        # TODO: check castling

        # update board
        board[location] = None
        board[new_location] = piece
        piece.has_moved = True

        # update en-passant
        new_row = int(new_location[1])
        old_row = int(location[1])
        if isinstance(piece, Pawn) and abs(new_row - old_row) == 2:
            # possible location of en-passant attacks
            board.en_passant = location[0] + str(old_row + (new_row - old_row) // 2)
        else:
            board.en_passant = None

        # update board history
        board.history.append(f'Moved {piece.color} {piece.name} from {location} to {new_location}.')

        # update turn
        if board.turn == 'white':
            board.turn = 'black'
        else:
            board.turn = 'white'

    @staticmethod
    def get_moves(board, location):
        """
        Gets the allowed moves for a piece in the specified location.
        Note that a piece cannot move to its current position.
        """
        # convert to upper case if user forgot
        location = location.upper()

        move_funcs = {
            King: GameMoves._king_moves,
            Queen: GameMoves._queen_moves,
            Rook: GameMoves._rook_moves,
            Bishop: GameMoves._bishop_moves,
            Knight: GameMoves._knight_moves,
            Pawn: GameMoves._pawn_moves,
        }

        piece = board[location]

        if piece is None:
            return list()
        else:
            move_func = move_funcs[type(piece)]
            return move_func(board, piece, location)

    @staticmethod
    def get_enemy_moves(board, enemy_color):
        """
        Returns all possible moves allowed by an enemy piece.
        """
        # determine all places the enemy can attack
        all_enemy_moves = list()
        for enemy_location, enemy_piece in board.items():
            if enemy_piece is not None and enemy_piece.color == enemy_color:
                if isinstance(enemy_piece, King):
                    enemy_moves = GameMoves._enemy_king_moves(board, enemy_location)
                elif isinstance(enemy_piece, Pawn):
                    enemy_moves = GameMoves._pawn_attack_moves(board, enemy_piece, enemy_location)
                else:
                    enemy_moves = GameMoves.get_moves(board, enemy_location)
                all_enemy_moves.extend(enemy_moves)
        return all_enemy_moves

    @staticmethod
    def _enemy_king_moves(board, location):
        """
        Simple check of where the enemy king can move.

        Note: Designed to avoid infinite recursion when friendly king checks possible moves of enemy king
        (which in turn would check possible moves of the friendly king).
        """
        # king's current location
        col = ord(location[0])
        row = int(location[1])

        # all locations within 1 move
        col_range = range(col - 1, col + 2)
        row_range = range(row - 1, row + 2)
        locations_to_check = [chr(c) + str(r) for r in row_range for c in col_range]

        # Simplified estimate of enemy king moves
        moves = list()
        for new_location in locations_to_check:
            try:
                board[new_location]
            except KeyError:  # new_location is out of range of the board
                continue
            else:
                moves.append(new_location)
        return moves

    @staticmethod
    def _king_moves(board, piece, location):
        """
        Moves allowed by the king
        """
        # king's current location
        col = ord(location[0])
        row = int(location[1])

        # all locations within 1 move
        col_range = range(col - 1, col + 2)
        row_range = range(row - 1, row + 2)
        locations_to_check = [chr(c) + str(r) for r in row_range for c in col_range]

        # determine all places the enemy can attack
        enemy_color = 'black' if piece.color == 'white' else 'white'
        all_enemy_moves = GameMoves.get_enemy_moves(board, enemy_color)

        # determine the valid moves
        moves = list()
        for new_location in locations_to_check:
            try:
                board[new_location]
            except KeyError:  # new_location is out of range of the board
                continue

            if new_location not in all_enemy_moves:
                # new_location must not be attackable by enemy
                if board[new_location] is None or board[new_location].color != piece.color:
                    # new_location must either be empty or occupied by enemy
                    moves.append(new_location)

        # TODO: Check for castling
        # if piece.color == 'white' and not piece.has_moved:  # check if white king can castle
        #     if board['A1'] is not None and not board['A1'].has_moved:
        #         # rook in A1 that hasn't moved
        #         if 'A3' not in all_enemy_moves and 'A4' not in all_enemy_moves:
        #             # king cannot be in check
        #             moves.append('A3')
        #     if board['A8']
        # elif piece.color == 'black' and not piece.has_moved:  # check if black king can castle
        #     pass
        return moves

    @staticmethod
    def _queen_moves(board, piece, location):
        """
        Moves allowed by a queen
        """
        rook_moves = GameMoves._rook_moves(board, piece, location)
        bishop_moves = GameMoves._bishop_moves(board, piece, location)
        queen_moves = list(set(rook_moves + bishop_moves))

        return queen_moves

    @staticmethod
    def _rook_moves(board, piece, location):
        """
        Moves allowed by a rook
        """
        # rook's current location
        col = ord(location[0])
        row = int(location[1])

        # possible moves
        moves = list()
        directions_to_check = {
            'right': lambda x: '%c%s' % (col + x, row),
            'left': lambda x: '%c%s' % (col - x, row),
            'up': lambda x: '%c%s' % (col, row + x),
            'down': lambda x: '%c%s' % (col, row - x),
        }
        for direction, move_rook in directions_to_check.items():
            for i in range(1, 8):  # a rook can move between 1 and 7 spaces at most
                new_location = move_rook(i)
                if new_location in board.keys() and board[new_location] is None:
                    moves.append(new_location)
                elif new_location in board.keys() and board[new_location].color != piece.color:
                    moves.append(new_location)
                    break
                else:
                    break

        return moves

    @staticmethod
    def _bishop_moves(board, piece, location):
        """
        Moves allowed by a bishop
        """
        # bishop's current location
        col = ord(location[0])
        row = int(location[1])

        # possible moves
        moves = list()
        directions_to_check = {
            'upper-right': lambda x: '%c%s' % (col + x, row + x),
            'lower-right': lambda x: '%c%s' % (col + x, row - x),
            'lower-left': lambda x: '%c%s' % (col - x, row - x),
            'upper-left': lambda x: '%c%s' % (col - x, row + x),
        }
        for direction, move_bishop in directions_to_check.items():
            for i in range(1, 8):  # a bishop can move between 1 and 7 spaces at most
                new_location = move_bishop(i)
                if new_location in board.keys() and board[new_location] is None:
                    moves.append(new_location)
                elif new_location in board.keys() and board[new_location].color != piece.color:
                    moves.append(new_location)
                    break
                else:
                    break

        return moves

    @staticmethod
    def _knight_moves(board, piece, location):
        """
        Moves allowed by a knight.
        """
        # knight's current location
        col = ord(location[0])
        row = int(location[1])

        # possible moves
        moves = [
            '%c%s' % (col - 1, row + 2),  # upper left
            '%c%s' % (col + 1, row + 2),  # upper right
            '%c%s' % (col + 2, row + 1),  # right upper
            '%c%s' % (col + 2, row - 1),  # right lower
            '%c%s' % (col + 1, row - 2),  # lower right
            '%c%s' % (col - 1, row - 2),  # lower left
            '%c%s' % (col - 2, row - 1),  # left lower
            '%c%s' % (col - 2, row + 1),  # left upper
        ]

        # verify possible move is on the board and not occupied by friendly piece
        for location in moves.copy():
            if location not in board.keys():
                moves.remove(location)
            elif board[location] is not None and board[location].color == piece.color:
                moves.remove(location)

        return moves

    @staticmethod
    def _pawn_moves(board, piece, location):
        """
        Moves allowed by a pawn
        """
        # pawns's current location
        col = location[0]
        row = location[1]
        if piece.color == 'white':
            direction = 1
        else:
            direction = -1

        moves = list()

        # check moving forward 1 space
        new_location = col + str(int(row) + direction)
        if board[new_location] is None:
            moves.append(new_location)

            # check moving forward 2 spaces
            if not piece.has_moved:
                new_location = col + str(int(row) + 2 * direction)
                if board[new_location] is None:
                    moves.append(new_location)

        # check attacks
        moves.extend(GameMoves._pawn_attack_moves(board, piece, location))
        return moves

    @staticmethod
    def _pawn_attack_moves(board, piece, location):
        """
        Attack moves allowed by a pawn.
        """
        # pawns's current location
        col = location[0]
        row = location[1]
        if piece.color == 'white':
            direction = 1
        else:
            direction = -1

        moves = list()

        # check attacks
        attack_cols = [chr(ord(col) - 1), chr(ord(col) + 1)]
        attack_row = str(int(row) + direction)
        locations_to_check = [attack_col + attack_row for attack_col in attack_cols]

        for new_location in locations_to_check:
            try:
                board[new_location]
            except KeyError:
                pass  # left side attack is off the board
            else:
                if board[new_location] is not None and board[new_location].color != piece.color:
                    moves.append(new_location)
                elif new_location == board.en_passant:
                    # checks en passant
                    moves.append(new_location)
        return moves
