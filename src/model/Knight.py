from typing import Tuple, List, override

import numpy as np

# from src.model.Board import Board
import src.model.Board as Board
from src.controller.CustomTypesForTypeHinting import ByteArray8x8
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum



class Knight(Piece):
    def __init__(self, color: ColorEnum, x: int, y: int):
        super().__init__(PieceTypeEnum.KNIGHT, color, x, y)


    # def get_possible_move(self, board: Board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    #     possible_moves = []
    #     protected_fields = []
    #     x = self.x
    #     y = self.y
    #     color = self.color
    #
    #     '''
    #     The board [yx] coordinates
    #
    #     [00][01][02][03][04][05][06][07]
    #     [10][11][12][13][14][15][16][17]
    #     [20][21][22][23][24][25][26][27]
    #     [30][31][32][33][34][35][36][37]
    #     [40][41][42][43][44][45][46][47]
    #     [50][51][52][53][54][55][56][57]
    #     [60][61][62][63][64][65][66][67]
    #     [70][71][72][73][74][75][76][77]
    #     '''
    #
    #     # Move forward
    #     if board.is_empty(x - 1, y - 2) or board.is_enemy(x - 1, y - 2, color):
    #         possible_moves.append((x - 1, y - 2))
    #     if board.is_empty(x + 1, y - 2) or board.is_enemy(x + 1, y - 2, color):
    #         possible_moves.append((x + 1, y - 2))
    #     if board.is_empty(x - 2, y - 1) or board.is_enemy(x - 2, y - 1, color):
    #         possible_moves.append((x - 2, y - 1))
    #     if board.is_empty(x + 2, y - 1) or board.is_enemy(x + 2, y - 1, color):
    #         possible_moves.append((x + 2, y - 1))
    #     if board.is_empty(x - 2, y + 1) or board.is_enemy(x - 2, y + 1, color):
    #         possible_moves.append((x - 2, y + 1))
    #     if board.is_empty(x + 2, y + 1) or board.is_enemy(x + 2, y + 1, color):
    #         possible_moves.append((x + 2, y + 1))
    #     if board.is_empty(x - 1, y + 2) or board.is_enemy(x - 1, y + 2, color):
    #         possible_moves.append((x - 1, y + 2))
    #     if board.is_empty(x + 1, y + 2) or board.is_enemy(x + 1, y + 2, color):
    #         possible_moves.append((x + 1, y + 2))
    #
    #     if board.is_friend(x - 1, y - 2, color):
    #         protected_fields.append((x - 1, y - 2))
    #     if board.is_friend(x + 1, y - 2, color):
    #         protected_fields.append((x + 1, y - 2))
    #     if board.is_friend(x - 2, y - 1, color):
    #         protected_fields.append((x - 2, y - 1))
    #     if board.is_friend(x + 2, y - 1, color):
    #         protected_fields.append((x + 2, y - 1))
    #     if board.is_friend(x - 2, y + 1, color):
    #         protected_fields.append((x - 2, y + 1))
    #     if board.is_friend(x + 2, y + 1, color):
    #         protected_fields.append((x + 2, y + 1))
    #     if board.is_friend(x - 1, y + 2, color):
    #         protected_fields.append((x - 1, y + 2))
    #     if board.is_friend(x + 1, y + 2, color):
    #         protected_fields.append((x + 1, y + 2))
    #
    #     return possible_moves, protected_fields

    @override
    def get_possible_moves(self, board: Board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:  # type: ignore
        possible_moves = []
        protected_fields = []
        x = self.x
        y = self.y
        color = self.color

        board: ByteArray8x8 = board.get_piece_board()

        move_pattern_list = [(x - 1, y - 2), (x + 1, y - 2), (x - 2, y - 1), (x + 2, y - 1),
                     (x - 2, y + 1), (x + 2, y + 1), (x - 1, y + 2), (x + 1, y + 2)]

        for move in move_pattern_list:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                field = board[move[1], move[0]]
                if color == ColorEnum.WHITE:
                    if field <= 0:
                        possible_moves.append(move)
                    else:
                        protected_fields.append(move)
                else:
                    if field >= 0:
                        possible_moves.append(move)
                    else:
                        protected_fields.append(move)


        return possible_moves, protected_fields


    # def get_possible_move(self, board: Board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
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
    #     def isin(_x, _y, fields):
    #         return np.any(np.all(fields == (_y, _x), axis=1))
    #
    #     if color == ColorEnum.WHITE:
    #         opponent_fields = black_fields
    #         friend_fields = white_fields
    #     else:
    #         opponent_fields = white_fields
    #         friend_fields = black_fields
    #
    #     # up left
    #     if isin(x - 1, y - 2, empty_fields) or isin(x - 1, y - 2, opponent_fields):
    #         possible_fields.append((x - 1, y - 2))
    #
    #     # up right
    #     if isin(x + 1, y - 2, empty_fields) or isin(x + 1, y - 2, opponent_fields):
    #         possible_fields.append((x + 1, y - 2))
    #
    #     # up left
    #     if isin(x - 2, y - 1, empty_fields) or isin(x - 2, y - 1, opponent_fields):
    #         possible_fields.append((x - 2, y - 1))
    #
    #     # up right
    #     if isin(x + 2, y - 1, empty_fields) or isin(x + 2, y - 1, opponent_fields):
    #         possible_fields.append((x + 2, y - 1))
    #
    #     # down left
    #     if isin(x - 2, y + 1, empty_fields) or isin(x - 2, y + 1, opponent_fields):
    #         possible_fields.append((x - 2, y + 1))
    #
    #     # down right
    #     if isin(x + 2, y + 1, empty_fields) or isin(x + 2, y + 1, opponent_fields):
    #         possible_fields.append((x + 2, y + 1))
    #
    #     # down left
    #     if isin(x - 1, y + 2, empty_fields) or isin(x - 1, y + 2, opponent_fields):
    #         possible_fields.append((x - 1, y + 2))
    #
    #     # down right
    #     if isin(x + 1, y + 2, empty_fields) or isin(x + 1, y + 2, opponent_fields):
    #         possible_fields.append((x + 1, y + 2))
    #
    #
    #     if isin(x - 1, y - 2, friend_fields):
    #         protected_fields.append((x - 1, y - 2))
    #     if isin(x + 1, y - 2, friend_fields):
    #         protected_fields.append((x + 1, y - 2))
    #     if isin(x - 2, y - 1, friend_fields):
    #         protected_fields.append((x - 2, y - 1))
    #     if isin(x + 2, y - 1, friend_fields):
    #         protected_fields.append((x + 2, y - 1))
    #     if isin(x - 2, y + 1, friend_fields):
    #         protected_fields.append((x - 2, y + 1))
    #     if isin(x + 2, y + 1, friend_fields):
    #         protected_fields.append((x + 2, y + 1))
    #     if isin(x - 1, y + 2, friend_fields):
    #         protected_fields.append((x - 1, y + 2))
    #     if isin(x + 1, y + 2, friend_fields):
    #         protected_fields.append((x + 1, y + 2))
    #
    #
    #     return possible_fields, protected_fields
    #

