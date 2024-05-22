from typing import Set, Tuple
from src.model.enums.enums import PieceType
import numpy as np


class PieceLogics:

    @staticmethod
    def get_attacked_fields(board, position) -> Set[Tuple[int, int]]:
        piece = board[position[0], position[1]]
        if abs(piece) == 1:
            return PieceLogics.pawn_attacked_fields(board, position)
        elif abs(piece) == 2:
            return PieceLogics.rook_attacked_fields(board, position)
        elif abs(piece) == 3:
            return PieceLogics.knight_attacked_fields(board, position)
        elif abs(piece) == 4:
            return PieceLogics.bishop_attacked_fields(board, position)
        elif abs(piece) == 5:
            return PieceLogics.queen_attacked_fields(board, position)
        elif abs(piece) == 6:
            return PieceLogics.king_attacked_fields(board, position)

    @staticmethod
    def pawn_attacked_fields(board, position) -> Set[Tuple[int, int]]:
        attacked_fields = set()
        is_white = board[position[0], position[1]] > 0
        row, col = position

        if is_white:
            if col - 1 >= 0 and row - 1 >= 0:
                if board[row - 1, col - 1] < 0:
                    attacked_fields.add((row - 1, col - 1))

            if col + 1 <= 7 and row - 1 >= 0:
                if board[row - 1, col + 1] < 0:
                    attacked_fields.add((row - 1, col + 1))
        else:
            if col - 1 >= 0 and row + 1 <= 7:
                if board[row + 1, col - 1] > 0:
                    attacked_fields.add((row + 1, col - 1))
            if col + 1 <= 7 and row + 1 <= 7:
                if board[row + 1, col + 1] > 0:
                    attacked_fields.add((row + 1, col + 1))

        return attacked_fields

    @staticmethod
    def rook_attacked_fields(board, position) -> Set[Tuple[int, int]]:
        attacked_fields = set()
        is_white = board[position[0], position[1]] > 0
        row, col = position

        vectors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        directions = [[(row + vector[0] * i, col + vector[1] * i) for i in range(1, 8)
                      if 0 <= row + vector[0] * i <= 7 and 0 <= col + vector[1] * i <= 7]
                      for vector in vectors]

        for direction in directions:
            for field in direction:
                if board[field[0], field[1]] == 0:
                    attacked_fields.add(field)
                # if field is occupied by opponent piece
                elif is_white and board[field[0], field[1]] < 0:
                    attacked_fields.add(field)
                    break
                elif not is_white and board[field[0], field[1]] > 0:
                    attacked_fields.add(field)
                    break
                # if field is occupied by friendly piece
                elif is_white and board[field[0], field[1]] > 0:
                    break
                elif not is_white and board[field[0], field[1]] < 0:
                    break

        return attacked_fields

    @staticmethod
    def knight_attacked_fields(board, position) -> Set[Tuple[int, int]]:
        attacked_fields = set()
        is_white = board[position[0], position[1]] > 0
        row, col = position

        move_pattern_list = [(row - 2, col - 1), (row - 2, col + 1), (row - 1, col - 2), (row - 1, col + 2),
                             (row + 1, col - 2), (row + 1, col + 2), (row + 2, col - 1), (row + 2, col + 1)]

        for field in move_pattern_list:
            if 0 <= field[0] <= 7 and 0 <= field[1] <= 7:
                # if field is empty
                if board[field[0], field[1]] == 0:
                    attacked_fields.add(field)
                # if adversary piece is on field
                elif is_white and board[field[0], field[1]] < 0:
                    attacked_fields.add(field)
                elif not is_white and board[field[0], field[1]] > 0:
                    attacked_fields.add(field)

        return attacked_fields

    @staticmethod
    def bishop_attacked_fields(board, position) -> Set[Tuple[int, int]]:
        attacked_fields = set()
        is_white = board[position[0], position[1]] > 0
        row, col = position

        vectors = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        directions = [[(row + vector[0] * i, col + vector[1] * i) for i in range(1, 8)
                       if 0 <= row + vector[0] * i <= 7 and 0 <= col + vector[1] * i <= 7]
                      for vector in vectors]

        for direction in directions:
            for field in direction:
                if board[field[0], field[1]] == 0:
                    attacked_fields.add(field)
                # if field is occupied by opponent piece
                elif is_white and board[field[0], field[1]] < 0:
                    attacked_fields.add(field)
                    break
                elif not is_white and board[field[0], field[1]] > 0:
                    attacked_fields.add(field)
                    break
                # if field is occupied by friendly piece
                elif is_white and board[field[0], field[1]] > 0:
                    break
                elif not is_white and board[field[0], field[1]] < 0:
                    break

        return attacked_fields

    @staticmethod
    def queen_attacked_fields(board, position) -> Set[Tuple[int, int]]:
        attacked_fields = set()
        is_white = board[position[0], position[1]] > 0
        row, col = position

        vectors = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        directions = [[(row + vector[0] * i, col + vector[1] * i) for i in range(1, 8)
                       if 0 <= row + vector[0] * i <= 7 and 0 <= col + vector[1] * i <= 7]
                      for vector in vectors]

        for direction in directions:
            for field in direction:
                if board[field[0], field[1]] == 0:
                    attacked_fields.add(field)
                # if field is occupied by opponent piece
                elif is_white and board[field[0], field[1]] < 0:
                    attacked_fields.add(field)
                    break
                elif not is_white and board[field[0], field[1]] > 0:
                    attacked_fields.add(field)
                    break
                # if field is occupied by friendly piece
                elif is_white and board[field[0], field[1]] > 0:
                    break
                elif not is_white and board[field[0], field[1]] < 0:
                    break

        return attacked_fields

    @staticmethod
    def king_attacked_fields(board, position) -> Set[Tuple[int, int]]:
        attacked_fields = set()
        is_white = board[position[0], position[1]] > 0
        row, col = position

        move_pattern_list = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col),
                             (row - 1, col - 1), (row + 1, col - 1), (row - 1, col + 1), (row + 1, col + 1)]

        for field in move_pattern_list:
            if 0 <= field[0] <= 7 and 0 <= field[1] <= 7:
                # if field is empty
                if board[field[0], field[1]] == 0:
                    attacked_fields.add(field)
                # if adversary piece is on field
                elif is_white and board[field[0], field[1]] < 0:
                    attacked_fields.add(field)
                elif not is_white and board[field[0], field[1]] > 0:
                    attacked_fields.add(field)

        return attacked_fields

    @staticmethod
    def get_possible_fields(board, position) -> Set[Tuple[int, int]]:
        piece_type = abs(board[position[0], position[1]])
        if piece_type == 1:
            unfiltered_fields = PieceLogics.get_pawn_possible_moves(board, position)
        else:
            unfiltered_fields = PieceLogics.get_attacked_fields(board, position)

        filtered_fields = set()
        for move in unfiltered_fields:
            if not PieceLogics.king_in_check_after_move(position, move, board):
                filtered_fields.add(move)

        return filtered_fields

    @staticmethod
    def king_in_check_after_move(from_position, to_position, board) -> bool:
        result = False

        from_row, from_col = from_position
        to_row, to_col = to_position
        moving_piece = board[from_row, from_col]
        captured_piece = board[to_row, to_col]
        is_white = moving_piece > 0

        board[to_row, to_col] = moving_piece

        if is_white:
            king_position = tuple(np.argwhere(board == 6)[0])
        else:
            king_position = tuple(np.argwhere(board == -6)[0])

        # Get opponent's attacked fields
        opponent_attacked_fields = PieceLogics.get_opponents_attacked_fields(board, is_white)
        if king_position in opponent_attacked_fields:
            result = True

        board[to_row, to_col] = captured_piece
        board[from_row, from_col] = moving_piece

        return result

    @staticmethod
    def get_opponents_attacked_fields(board, is_white) -> Set[Tuple[int, int]]:
        # Initialize an empty set to store the attacked fields
        attacked_fields = set()

        # Get the positions of the opponent's pieces
        if is_white:
            opponent_pieces_positions = np.argwhere(board < 0)
        else:
            opponent_pieces_positions = np.argwhere(board > 0)

        # For each opponent piece, calculate the fields it can attack
        for position in opponent_pieces_positions:
            piece_type = abs(board[tuple(position)])
            if piece_type == 1:
                attacked_fields.update(PieceLogics.pawn_attacked_fields(board, tuple(position)))
            elif piece_type == 2:
                attacked_fields.update(PieceLogics.rook_attacked_fields(board, tuple(position)))
            elif piece_type == 3:
                attacked_fields.update(PieceLogics.knight_attacked_fields(board, tuple(position)))
            elif piece_type == 4:
                attacked_fields.update(PieceLogics.bishop_attacked_fields(board, tuple(position)))
            elif piece_type == 5:
                attacked_fields.update(PieceLogics.queen_attacked_fields(board, tuple(position)))
            elif piece_type == 6:
                attacked_fields.update(PieceLogics.king_attacked_fields(board, tuple(position)))

        return attacked_fields

    @staticmethod
    def get_pawn_possible_moves(board, position) -> Set[Tuple[int, int]]:
        possible_fields = set()
        is_white = board[position[0], position[1]] > 0
        row, col = position

        # Move forward
        if is_white:
            if row - 1 >= 0:
                if board[row - 1, col] == 0:
                    possible_fields.add((row - 1, col))
        else:
            if row + 1 <= 7:
                if board[row + 1, col] == 0:
                    possible_fields.add((row + 1, col))

        # Move two squares forward
        if is_white and row == 6:
            if board[row - 1, col] == 0 and board[row - 2, col] == 0:
                possible_fields.add((row - 2, col))
        elif not is_white and row == 1:
            if board[row + 1, col] == 0 and board[row + 2, col] == 0:
                possible_fields.add((row + 2, col))

        # Diagonal capture
        if is_white:
            if col - 1 >= 0 and row - 1 >= 0:
                if board[row - 1, col - 1] < 0:
                    possible_fields.add((row - 1, col - 1))
            if col + 1 <= 7 and row - 1 >= 0:
                if board[row - 1, col + 1] < 0:
                    possible_fields.add((row - 1, col + 1))
        else:
            if col - 1 >= 0 and row + 1 <= 7:
                if board[row + 1, col - 1] > 0:
                    possible_fields.add((row + 1, col - 1))

            if col + 1 <= 7 and row + 1 <= 7:
                if board[row + 1, col + 1] > 0:
                    possible_fields.add((row + 1, col + 1))

        # # Add en passant if possible
        # if last_moved_piece is not None and \
        #         isinstance(last_moved_piece, Pawn) and \
        #         last_moved_piece.is_en_passant and \
        #         self.row == last_moved_piece.row and \
        #         abs(self.col - last_moved_piece.col) == 1:
        #     # print("En passant move is added.")
        #     if self._color == Color.W:
        #         possible_fields.add((last_moved_piece.row - 1, last_moved_piece.col))
        #     else:
        #         possible_fields.add((last_moved_piece.row + 1, last_moved_piece.col))

        return possible_fields
