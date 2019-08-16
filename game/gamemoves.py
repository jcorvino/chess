from game.pieces import King, Queen, Rook, Bishop, Knight, Pawn


class GameMoves:
    """
    Class to determine which moves are allowed and to move pieces.
    """

    @staticmethod
    def get_moves(gameboard, location):
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

        piece = gameboard.board[location]

        if piece is None:
            return list()
        else:
            move_func = move_funcs[type(piece)]
            print(piece, location)
            return move_func(gameboard, piece, location)

    @staticmethod
    def get_enemy_moves(gameboard, enemy_color):
        """
        Returns all possible moves allowed by an enemy piece.
        """
        # determine all places the enemy can attack
        all_enemy_moves = list()
        for enemy_location, enemy_piece in gameboard.board.items():
            if enemy_piece is not None and enemy_piece.color == enemy_color:
                if isinstance(enemy_piece, King):
                    enemy_moves = GameMoves._enemy_king_moves(gameboard, enemy_piece, enemy_location)
                elif isinstance(enemy_piece, Pawn):
                    enemy_moves = GameMoves._pawn_attack_moves(gameboard, enemy_piece, enemy_location)
                else:
                    enemy_moves = GameMoves.get_moves(gameboard, enemy_location)
                all_enemy_moves.extend(enemy_moves)
        return all_enemy_moves

    @staticmethod
    def _enemy_king_moves(gameboard, piece, location):
        """
        Simple check of where the enemy king can move.

        Note: Designed to avoid infinite recursion when friendly king checks possible moves of enemy king
        (which in turn would check possible moves of the friendly king).
        """
        # king's current location
        col = location[0]
        row = location[1]

        # all locations within 1 move
        col_range = range(ord(col) - 1, ord(col) + 2)
        row_range = range(int(row) - 1, int(row) + 2)
        locations_to_check = [chr(c) + str(r) for r in row_range for c in col_range]

        # Simplified estimate of enemy king moves
        moves = list()
        for new_location in locations_to_check:
            try:
                gameboard.board[new_location]
            except KeyError:  # new_location is out of range of the board
                continue
            else:
                moves.append(new_location)
        return moves

    @staticmethod
    def _king_moves(gameboard, piece, location):
        """
        Moves allowed by the king
        """
        # king's current location
        col = location[0]
        row = location[1]

        # all locations within 1 move
        col_range = range(ord(col) - 1, ord(col) + 2)
        row_range = range(int(row) - 1, int(row) + 2)
        locations_to_check = [chr(c) + str(r) for r in row_range for c in col_range]

        # determine all places the enemy can attack
        enemy_color = 'black' if piece.color == 'white' else 'white'
        all_enemy_moves = GameMoves.get_enemy_moves(gameboard, enemy_color)

        # determine the valid moves
        moves = list()
        for new_location in locations_to_check:
            try:
                gameboard.board[new_location]
            except KeyError:  # new_location is out of range of the board
                continue

            if new_location not in all_enemy_moves:
                # new_location must not be attackable by enemy
                if gameboard.board[new_location] is None or gameboard.board[new_location].color != piece.color:
                    # new_location must either be empty or occupied by enemy
                    moves.append(new_location)

        # TODO: Check for castling
        # if piece.color == 'white' and not piece.has_moved:  # check if white king can castle
        #     if gameboard.board['A1'] is not None and not gameboard.board['A1'].has_moved:
        #         # rook in A1 that hasn't moved
        #         if 'A3' not in all_enemy_moves and 'A4' not in all_enemy_moves:
        #             # king cannot be in check
        #             moves.append('A3')
        #     if gameboard.board['A8']
        # elif piece.color == 'black' and not piece.has_moved:  # check if black king can castle
        #     pass
        return moves

    @staticmethod
    def _queen_moves(gameboard, piece, location):
        return list()

    @staticmethod
    def _rook_moves(gameboard, piece, location):
        return list()

    @staticmethod
    def _bishop_moves(gameboard, piece, location):
        return list()

    @staticmethod
    def _knight_moves(gameboard, piece, location):
        """
        Moves allowed by a knight.
        """
        # knight's current location
        col = ord(location[0])
        row = int(location[1])

        moves = list()

        # possible moves
        moves.append('%c%s' % (col - 1, row + 2))  # upper left
        moves.append('%c%s' % (col + 1, row + 2))  # upper right
        moves.append('%c%s' % (col + 2, row + 1))  # right upper
        moves.append('%c%s' % (col + 2, row - 1))  # right lower
        moves.append('%c%s' % (col + 1, row - 2))  # lower right
        moves.append('%c%s' % (col - 1, row - 2))  # lower left
        moves.append('%c%s' % (col - 2, row - 1))  # left lower
        moves.append('%c%s' % (col - 2, row + 1))  # left upper

        # verify possible move is on the board and not occupied by friendly piece
        for location in moves.copy():
            if location not in gameboard.board.keys():
                moves.remove(location)

            elif gameboard.board[location] is not None and gameboard.board[location].color == piece.color:
                moves.remove(location)

        return moves

    @staticmethod
    def _pawn_moves(gameboard, piece, location):
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
        if gameboard.board[new_location] is None:
            moves.append(new_location)

            # check moving forward 2 spaces
            if not piece.has_moved:
                new_location = col + str(int(row) + 2 * direction)
                if gameboard.board[new_location] is None:
                    moves.append(new_location)

        # check attacks
        moves.extend(GameMoves._pawn_attack_moves(gameboard, piece, location))
        return moves

    @staticmethod
    def _pawn_attack_moves(gameboard, piece, location):
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
        #TODO: Check for en passant
        for new_location in locations_to_check:
            try:
                gameboard.board[new_location]
            except KeyError:
                pass  # left side attack is off the board
            else:
                if gameboard.board[new_location] is not None and gameboard.board[new_location].color != piece.color:
                    moves.append(new_location)
        return moves


if __name__ == '__main__':
    from game.board import GameBoard
    gb = GameBoard()
    print(gb.board.keys())
    print(GameMoves.get_moves(gb, 'H1'))
