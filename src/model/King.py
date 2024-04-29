import functools
import time
from typing import override, Tuple, List

import numpy as np

from src.controller.CustomTypesForTypeHinting import ByteArray8x8
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.KING, color, x, y)

    # @override
    # def get_possible_move(self, board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    #     possible_fields = []
    #     protected_fields = []
    #     x = self.x
    #     y = self.y
    #     color = self.color
    #
    #     # Move vertically
    #     if board.is_empty(x, y - 1) or board.is_enemy(x, y - 1, color):
    #         possible_fields.append((x, y - 1))
    #     elif board.is_friend(x, y - 1, color):
    #         protected_fields.append((x, y - 1))
    #
    #     # Move vertically
    #     if board.is_empty(x, y + 1) or board.is_enemy(x, y + 1, color):
    #         possible_fields.append((x, y + 1))
    #     elif board.is_friend(x, y + 1, color):
    #         protected_fields.append((x, y + 1))
    #
    #     # Move horizontally
    #     if board.is_empty(x - 1, y) or board.is_enemy(x - 1, y, color):
    #         possible_fields.append((x - 1, y))
    #     elif board.is_friend(x - 1, y, color):
    #         protected_fields.append((x - 1, y))
    #
    #     # Move horizontally
    #     if board.is_empty(x + 1, y) or board.is_enemy(x + 1, y, color):
    #         possible_fields.append((x + 1, y))
    #     elif board.is_friend(x + 1, y, color):
    #         protected_fields.append((x + 1, y))
    #
    #     # Move diagonally
    #     if board.is_empty(x - 1, y - 1) or board.is_enemy(x - 1, y - 1, color):
    #         possible_fields.append((x - 1, y - 1))
    #     elif board.is_friend(x - 1, y - 1, color):
    #         protected_fields.append((x - 1, y - 1))
    #
    #     # Move diagonally
    #     if board.is_empty(x + 1, y - 1) or board.is_enemy(x + 1, y - 1, color):
    #         possible_fields.append((x + 1, y - 1))
    #     elif board.is_friend(x + 1, y - 1, color):
    #         protected_fields.append((x + 1, y - 1))
    #
    #     # Move diagonally
    #     if board.is_empty(x - 1, y + 1) or board.is_enemy(x - 1, y + 1, color):
    #         possible_fields.append((x - 1, y + 1))
    #     elif board.is_friend(x - 1, y + 1, color):
    #         protected_fields.append((x - 1, y + 1))
    #
    #     # Move diagonally
    #     if board.is_empty(x + 1, y + 1) or board.is_enemy(x + 1, y + 1, color):
    #         possible_fields.append((x + 1, y + 1))
    #     elif board.is_friend(x + 1, y + 1, color):
    #         protected_fields.append((x + 1, y + 1))
    #
    #     for field in possible_fields:
    #         # if field in board._opponent_player.attacked_fields:
    #         #     possible_fields.remove(field)
    #
    #         if color == ColorEnum.WHITE:
    #             if board.square_is_attacked_by_black(field[0], field[1]) or \
    #                     board.square_is_protected_by_black(field[0], field[1]):
    #                 possible_fields.remove(field)
    #         else:
    #             if board.square_is_attacked_by_white(field[0], field[1]) or \
    #                     board.square_is_protected_by_white(field[0], field[1]):
    #                 possible_fields.remove(field)
    #
    #     return possible_fields, protected_fields

    @override
    def get_possible_moves(self, board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        possible_moves = []
        protected_fields = []
        x = self.x
        y = self.y
        color = self.color

        board: ByteArray8x8 = board.get_piece_board()

        move_pattern_list = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y),
                             (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]

        for move in move_pattern_list:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                field = board[move[1], move[0]]

                if color == ColorEnum.WHITE and field <= 0:
                    possible_moves.append(move)
                elif color == ColorEnum.BLACK and field >= 0:
                    possible_moves.append(move)

                if color == ColorEnum.WHITE and field > 0:
                    protected_fields.append(move)
                elif color == ColorEnum.BLACK and field < 0:
                    protected_fields.append(move)


        return possible_moves, protected_fields

    # @override
    # def get_possible_moves(self, board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    #     possible_fields = []
    #     protected_fields = []
    #     x = self.x
    #     y = self.y
    #     color = self.color
    #
    #     board = board.get_piece_board()
    #
    #     # Fields: (y, x) -> (row, column)
    #     empty_fields = np.dstack(np.where(board == 0))[0]
    #     white_fields = np.dstack(np.where(board > 0))[0]
    #     black_fields = np.dstack(np.where(board < 0))[0]
    #
    #     def isin(_y, _x, fields):
    #         return np.any(np.all(fields == (_y, _x), axis=1))
    #
    #     if color == ColorEnum.WHITE:
    #         opponent_fields = black_fields
    #         friend_fields = white_fields
    #     else:
    #         opponent_fields = white_fields
    #         friend_fields = black_fields
    #
    #     # Move vertically
    #     if isin(y - 1, x, empty_fields) or isin(y - 1, x, opponent_fields):
    #         possible_fields.append((x, y - 1))
    #     elif isin(y - 1, x, friend_fields):
    #         protected_fields.append((x, y - 1))
    #
    #     if isin(y + 1, x, empty_fields) or isin(y + 1, x, opponent_fields):
    #         possible_fields.append((x, y + 1))
    #     elif isin(y + 1, x, friend_fields):
    #         protected_fields.append((x, y + 1))
    #
    #     if isin(y, x - 1, empty_fields) or isin(y, x - 1, opponent_fields):
    #         possible_fields.append((x - 1, y))
    #     elif isin(y, x - 1, friend_fields):
    #         protected_fields.append((x - 1, y))
    #
    #     if isin(y, x + 1, empty_fields) or isin(y, x + 1, opponent_fields):
    #         possible_fields.append((x + 1, y))
    #     elif isin(y, x + 1, friend_fields):
    #         protected_fields.append((x + 1, y))
    #
    #     if isin(y - 1, x - 1, empty_fields) or isin(y - 1, x - 1, opponent_fields):
    #         possible_fields.append((x - 1, y - 1))
    #     elif isin(y - 1, x - 1, friend_fields):
    #         protected_fields.append((x - 1, y - 1))
    #
    #     if isin(y - 1, x + 1, empty_fields) or isin(y - 1, x + 1, opponent_fields):
    #         possible_fields.append((x + 1, y - 1))
    #     elif isin(y - 1, x + 1, friend_fields):
    #         protected_fields.append((x + 1, y - 1))
    #
    #     if isin(y + 1, x - 1, empty_fields) or isin(y + 1, x - 1, opponent_fields):
    #         possible_fields.append((x - 1, y + 1))
    #     elif isin(y + 1, x - 1, friend_fields):
    #         protected_fields.append((x - 1, y + 1))
    #
    #     if isin(y + 1, x + 1, empty_fields) or isin(y + 1, x + 1, opponent_fields):
    #         possible_fields.append((x + 1, y + 1))
    #     elif isin(y + 1, x + 1, friend_fields):
    #         protected_fields.append((x + 1, y + 1))
    #
    #
    #     return possible_fields, protected_fields


