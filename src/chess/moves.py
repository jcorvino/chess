from .pieces import King, Queen, Rook, Bishop, Knight, Pawn, GamePiece
from .board import GameBoard, Location, Locations, Color


class GameMoves:
    """
    Class to determine which moves are allowed and to move pieces.
    """

    @staticmethod
    def move(board: GameBoard, old_location: Location, new_location: Location) -> None:
        """
        Move a piece on the board from old_location to new_location
        """
        # convert to upper case if user forgot
        new_location = new_location.upper()
        old_location = old_location.upper()

        # check if valid game piece
        piece = board[old_location]
        if piece is None:
            raise ValueError(f'No piece at {old_location}')

        # check if correct color
        if piece.color != board.turn:
            raise ValueError(f'Cannot move piece at {old_location}! It is not {piece.color}\'s turn')

        # check allowed moves
        valid_moves = GameMoves.get_moves(board, old_location)
        if new_location not in valid_moves:
            raise ValueError(f'Moving {piece.name} to {new_location} is not a valid move. Check get_moves function.')

        # TODO: check castling
        # TODO: check for check

        # update board
        board[old_location] = None
        board[new_location] = piece
        piece.has_moved = True

        # update en-passant
        new_row = int(new_location[1])
        old_row = int(old_location[1])
        if isinstance(piece, Pawn) and abs(new_row - old_row) == 2:
            # possible location of en-passant attacks
            board.en_passant = old_location[0] + str(old_row + (new_row - old_row) // 2)
        else:
            board.en_passant = None

        # update board history
        board.history.append(f'Moved {piece.color} {piece.name} from {old_location} to {new_location}.')

        # update turn
        board.turn = 'black' if board.turn == 'white' else 'white'

    @staticmethod
    def in_check(board: GameBoard, color: Color) -> bool:
        """
        Check if the specified color is in check
        """
        return False

    @staticmethod
    def get_moves(board: GameBoard, location: Location) -> Locations:
        """
        Gets the allowed moves for a piece in the specified location.
        Note that a piece cannot move to its current position.
        """
        # TODO: Check for check
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
            return set()
        else:
            move_func = move_funcs[type(piece)]
            return move_func(board, piece, location)

    @staticmethod
    def get_all_attacks(board: GameBoard, color: Color, simple_king: bool = False) -> Locations:
        """
        Returns all possible attacks allowed by the specified color.
        """
        # determine all places the player can attack
        all_attacks = set()
        for location, piece in board.items():
            if piece and piece.color == color:
                if isinstance(piece, King):
                    if simple_king:
                        attacks = GameMoves._simple_king_moves(board, location)
                    else:
                        attacks = GameMoves._king_moves(board, location)
                elif isinstance(piece, Pawn):
                    attacks = GameMoves._pawn_attack_moves(board, piece, location)
                else:
                    attacks = GameMoves.get_moves(board, location)
                all_attacks.update(attacks)
        return all_attacks

    @staticmethod
    def get_all_moves(board: GameBoard, color: Color) -> Locations:
        """
        Returns all possible moves allowed by the specified color.
        """
        all_moves = GameMoves.get_all_attacks(board, color)

        # Add pawn moves that are not attacks
        for location, piece in board.items():
            if piece and piece.color == color:
                if isinstance(piece, Pawn):
                    all_moves.update(GameMoves._pawn_attack_moves(board, piece, location))
        return all_moves

    @staticmethod
    def _simple_king_moves(board: GameBoard, location: Location) -> Locations:
        """
        Simple check of where the king can move.

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
        # TODO: Improve so it correctly shows spots that are blocked by friendly pieces or enemy king's range
        moves = set()
        for new_location in locations_to_check:
            try:
                board[new_location]
            except KeyError:  # new_location is out of range of the board
                continue
            else:
                moves.add(new_location)
        return moves

    @staticmethod
    def _king_moves(board: GameBoard, piece: GamePiece, location: Location) -> Locations:
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
        all_enemy_attacks = GameMoves.get_all_attacks(board, enemy_color, simple_king=True)

        # determine the valid moves
        moves = set()
        for new_location in locations_to_check:
            try:
                board[new_location]
            except KeyError:  # new_location is out of range of the board
                continue

            if new_location not in all_enemy_attacks:
                # new_location must not be attackable by enemy
                if board[new_location] is None or board[new_location].color != piece.color:
                    # new_location must either be empty or occupied by enemy
                    moves.add(new_location)

        # Check for castling
        moves.update(GameMoves._castle_moves(board, piece, location))
        return moves

    @staticmethod
    def _castle_moves(board: GameBoard, piece: GamePiece, location: Location) -> Locations:
        """
        Castle moves allowed by the king.
        """
        # king's current location
        col = ord(location[0])
        row = int(location[1])

        # TODO: Check for castling
        # TODO: determine if king is in check
        if not piece.has_moved:
            left_rook = board['A' + str(row)]
            right_rook = board['H' + str(row)]
        for rook in [left_rook, right_rook]:
            if rook and rook.color == piece.color and not rook.has_moved:
                # Rook can castle.
                # Verify no blocking pieces
                # Verify King doesn't pass through check.
                # Verify King is not currently in check
                pass
        moves = set()
        return moves

    @staticmethod
    def _queen_moves(board: GameBoard, piece: GamePiece, location: Location) -> Locations:
        """
        Moves allowed by a queen
        """
        rook_moves = GameMoves._rook_moves(board, piece, location)
        bishop_moves = GameMoves._bishop_moves(board, piece, location)
        queen_moves = rook_moves | bishop_moves  # union
        return queen_moves

    @staticmethod
    def _rook_moves(board: GameBoard, piece: GamePiece, location: Location) -> Locations:
        """
        Moves allowed by a rook
        """
        # rook's current location
        col = ord(location[0])
        row = int(location[1])

        # possible moves
        moves = set()
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
                    moves.add(new_location)
                elif new_location in board.keys() and board[new_location].color != piece.color:
                    moves.add(new_location)
                    break
                else:
                    break

        return moves

    @staticmethod
    def _bishop_moves(board: GameBoard, piece: GamePiece, location: Location) -> Locations:
        """
        Moves allowed by a bishop
        """
        # bishop's current location
        col = ord(location[0])
        row = int(location[1])

        # possible moves
        moves = set()
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
                    moves.add(new_location)
                elif new_location in board.keys() and board[new_location].color != piece.color:
                    moves.add(new_location)
                    break
                else:
                    break

        return moves

    @staticmethod
    def _knight_moves(board: GameBoard, piece: GamePiece, location: Location) -> Locations:
        """
        Moves allowed by a knight.
        """
        # knight's current location
        col = ord(location[0])
        row = int(location[1])

        # possible moves
        moves = {
            '%c%s' % (col - 1, row + 2),  # upper left
            '%c%s' % (col + 1, row + 2),  # upper right
            '%c%s' % (col + 2, row + 1),  # right upper
            '%c%s' % (col + 2, row - 1),  # right lower
            '%c%s' % (col + 1, row - 2),  # lower right
            '%c%s' % (col - 1, row - 2),  # lower left
            '%c%s' % (col - 2, row - 1),  # left lower
            '%c%s' % (col - 2, row + 1),  # left upper
        }  # type: Locations

        # verify possible move is on the board and not occupied by friendly piece
        for location in moves.copy():
            if location not in board.keys():
                moves.remove(location)
            elif board[location] is not None and board[location].color == piece.color:
                moves.remove(location)

        return moves

    @staticmethod
    def _pawn_moves(board: GameBoard, piece: GamePiece, location: Location) -> Locations:
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

        moves = set()

        # check moving forward 1 space
        new_location = col + str(int(row) + direction)
        if board[new_location] is None:
            moves.add(new_location)

            # check moving forward 2 spaces
            if not piece.has_moved:
                new_location = col + str(int(row) + 2 * direction)
                if board[new_location] is None:
                    moves.add(new_location)

        # check attacks
        return moves.union(GameMoves._pawn_attack_moves(board, piece, location))

    @staticmethod
    def _pawn_attack_moves(board: GameBoard, piece: GamePiece, location: Location) -> Locations:
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

        moves = set()

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
                    moves.add(new_location)
                elif new_location == board.en_passant:
                    # checks en passant
                    moves.add(new_location)
        return moves
