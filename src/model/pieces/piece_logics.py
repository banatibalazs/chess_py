from typing import Set, Tuple, List, Optional

from src.controller.custom_types_for_type_hinting import ByteArray8x8
from src.model.enums.enums import PieceType
import numpy as np


class PieceLogics:

    @staticmethod
    def get_attacked_fields(board, position, is_white) -> Set[Tuple[int, int]]:
        piece = board[position[0], position[1]]
        if abs(piece) == 1:
            return PieceLogics.pawn_attacked_fields(board, position, is_white)
        elif abs(piece) == 2:
            return PieceLogics.rook_attacked_fields(board, position, is_white)
        elif abs(piece) == 3:
            return PieceLogics.knight_attacked_fields(board, position, is_white)
        elif abs(piece) == 4:
            return PieceLogics.bishop_attacked_fields(board, position, is_white)
        elif abs(piece) == 5:
            return PieceLogics.queen_attacked_fields(board, position, is_white)
        elif abs(piece) == 6:
            return PieceLogics.king_attacked_fields(board, position, is_white)

    @staticmethod
    def pawn_attacked_fields(board, position, is_white) -> Set[Tuple[int, int]]:
        attacked_fields = set()
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
    def rook_attacked_fields(board, position, is_white) -> Set[Tuple[int, int]]:
        attacked_fields = set()
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
    def knight_attacked_fields(board, position, is_white) -> Set[Tuple[int, int]]:
        attacked_fields = set()
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
    def bishop_attacked_fields(board, position, is_white) -> Set[Tuple[int, int]]:
        attacked_fields = set()
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
    def queen_attacked_fields(board, position, is_white) -> Set[Tuple[int, int]]:
        attacked_fields = set()
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
    def king_attacked_fields(board, position, is_white) -> Set[Tuple[int, int]]:
        attacked_fields = set()
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
    def get_possible_moves_of_piece(board: ByteArray8x8, position: Tuple[int, int],
                                    king_04_is_moved: bool, king_74_is_moved: bool, rook_00_is_moved: bool,
                                    rook_07_is_moved: bool, rook_70_is_moved: bool, rook_77_is_moved: bool,
                                    is_en_passant, last_move) -> Set[Tuple[int, int]]:
        piece_type = abs(board[position[0], position[1]])
        is_white = board[position[0], position[1]] > 0

        if piece_type == 1:
            unfiltered_fields = PieceLogics.get_pawn_possible_moves(board, position, is_white,
                                                                    is_en_passant, last_move)
        else:
            unfiltered_fields = PieceLogics.get_attacked_fields(board, position, is_white)
        if piece_type == 6:
            unfiltered_fields.update(PieceLogics.get_castling_moves(board, king_04_is_moved,
                                                                    king_74_is_moved, rook_00_is_moved,
                                                                    rook_07_is_moved, rook_70_is_moved,
                                                                    rook_77_is_moved, is_white))

        filtered_fields = set()
        for move in unfiltered_fields:
            if not PieceLogics.king_in_check_after_move(position, move, board):
                filtered_fields.add(move)
        return filtered_fields

    @staticmethod
    def king_in_check_after_move(from_position: Tuple[int, int],
                                 to_position: Tuple[int, int],
                                 board: ByteArray8x8) -> bool:
        result = False
        from_row, from_col = from_position
        to_row, to_col = to_position

        # save the moving piece
        moving_piece = board[from_row, from_col]
        # save the captured piece
        captured_piece = board[to_row, to_col]
        # move the piece
        board[from_row, from_col] = 0
        board[to_row, to_col] = moving_piece

        is_white = moving_piece > 0

        king_position = tuple(np.argwhere(board == 6)[0]) if is_white else tuple(np.argwhere(board == -6)[0])
        # Get opponent's attacked fields
        opponent_attacked_fields = PieceLogics.get_opponents_attacked_fields(board, is_white)
        if king_position in opponent_attacked_fields:
            result = True

        board[to_row, to_col] = captured_piece
        board[from_row, from_col] = moving_piece

        return result

    @staticmethod
    def get_opponents_attacked_fields(board: ByteArray8x8, is_white: bool) -> Set[Tuple[int, int]]:

        # Get the positions of the opponent's pieces
        if is_white:
            opponent_pieces_positions = np.argwhere(board < 0)
        else:
            opponent_pieces_positions = np.argwhere(board > 0)

        # For each opponent piece, calculate the fields it can attack
        attacked_fields = set()
        for position in opponent_pieces_positions:
            piece_type = abs(board[tuple(position)])
            if piece_type == 1:
                attacked_fields.update(PieceLogics.pawn_attacked_fields(board, tuple(position), not is_white))
            elif piece_type == 2:
                attacked_fields.update(PieceLogics.rook_attacked_fields(board, tuple(position), not is_white))
            elif piece_type == 3:
                attacked_fields.update(PieceLogics.knight_attacked_fields(board, tuple(position), not is_white))
            elif piece_type == 4:
                attacked_fields.update(PieceLogics.bishop_attacked_fields(board, tuple(position), not is_white))
            elif piece_type == 5:
                attacked_fields.update(PieceLogics.queen_attacked_fields(board, tuple(position), not is_white))
            elif piece_type == 6:
                attacked_fields.update(PieceLogics.king_attacked_fields(board, tuple(position), not is_white))

        return attacked_fields

    @staticmethod
    def get_all_possible_moves(board, is_white, king_04_is_moved, king_74_is_moved, rook_00_is_moved,
                               rook_07_is_moved, rook_70_is_moved, rook_77_is_moved, is_en_passant, last_move):

        piece_positions = np.argwhere(board > 0) if is_white else np.argwhere(board < 0)
        possible_moves = set()
        for pos in piece_positions:
            possible_moves.update(PieceLogics.get_possible_moves_of_piece(board, pos,
                                                                          king_04_is_moved, king_74_is_moved,
                                                                          rook_00_is_moved, rook_07_is_moved,
                                                                          rook_70_is_moved, rook_77_is_moved,
                                                                          is_en_passant, last_move))
        return possible_moves

    @staticmethod
    def get_pawn_possible_moves(board, position, is_white, is_en_passant, last_move) -> Set[Tuple[int, int]]:
        possible_fields = set()
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

        # Add en passant if possible
        if last_move is not None:
            _, _, last_move_to_row, last_move_to_col = last_move
            if is_en_passant and row == last_move_to_row and abs(col - last_move_to_col) == 1:
                print("En passant move is added.")
                if is_white:
                    possible_fields.add((last_move_to_row - 1, last_move_to_col))
                else:
                    possible_fields.add((last_move_to_row + 1, last_move_to_col))

        return possible_fields

    @staticmethod
    def get_castling_moves(board, king_04_is_moved, king_74_is_moved, rook_00_is_moved,
                           rook_07_is_moved, rook_70_is_moved, rook_77_is_moved, is_white) -> Optional[Set[Tuple[int, int]]]:

        opponent_attacked_fields = PieceLogics.get_opponents_attacked_fields(board, is_white)
        possible_fields = set()
        if is_white:
            if not king_74_is_moved and not rook_70_is_moved:
                if board[7, 0] == 2 and board[7, 1] == 0 and board[7, 2] == 0 and board[7, 3] == 0:
                    if (7, 0) not in opponent_attacked_fields and (7, 1) not in opponent_attacked_fields and (
                            7, 2) not in opponent_attacked_fields and (7, 4) not in opponent_attacked_fields:
                        possible_fields.add((7, 2))
            if not king_74_is_moved and not rook_77_is_moved:
                if board[7, 7] == 2 and board[7, 6] == 0 and board[7, 5] == 0:
                    if (7, 4) not in opponent_attacked_fields and (7, 5) not in opponent_attacked_fields and (
                            7, 6) not in opponent_attacked_fields and (7, 4) not in opponent_attacked_fields:
                        possible_fields.add((7, 6))
        else:
            if not king_04_is_moved and not rook_00_is_moved:
                if board[0, 0] == -2 and board[0, 1] == 0 and board[0, 2] == 0 and board[0, 3] == 0:
                    if (0, 0) not in opponent_attacked_fields and (0, 1) not in opponent_attacked_fields and (
                            0, 2) not in opponent_attacked_fields and (0, 4) not in opponent_attacked_fields:
                        possible_fields.add((0, 2))
            if not king_04_is_moved and not rook_07_is_moved:
                if board[0, 7] == -2 and board[0, 6] == 0 and board[0, 5] == 0:
                    if (0, 4) not in opponent_attacked_fields and (0, 5) not in opponent_attacked_fields and (
                            0, 6) not in opponent_attacked_fields and (0, 4) not in opponent_attacked_fields:
                        possible_fields.add((0, 6))

        return possible_fields

