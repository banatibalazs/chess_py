from typing import List, Tuple, override
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Pawn(Piece):
    def __init__(self, color: ColorEnum, x: int, y: int):
        super().__init__(PieceTypeEnum.PAWN, color, x, y)
        self._is_en_passant = False

    @override
    def get_possible_moves(self, board: Board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        possible_fields = []
        protected_fields = []
        x = self.x
        y = self.y
        color = self.color

        piece_board = board.get_piece_board()

        # Move forward
        if color == ColorEnum.WHITE:
            if y - 1 >= 0:
                if piece_board[y - 1, x] == 0:
                    possible_fields.append((x, y - 1))
        else:
            if y + 1 <= 7:
                if piece_board[y + 1, x] == 0:
                    possible_fields.append((x, y + 1))

        # Move two squares forward
        if color == ColorEnum.WHITE and y == 6:
            if piece_board[y - 1, x] == 0 and piece_board[y - 2, x] == 0:
                possible_fields.append((x, y - 2))
        elif color == ColorEnum.BLACK and y == 1:
            if piece_board[y + 1, x] == 0 and piece_board[y + 2, x] == 0:
                possible_fields.append((x, y + 2))

        # Diagonal capture
        if color == ColorEnum.WHITE:
            if x - 1 >= 0 and y - 1 >= 0:
                if piece_board[y - 1, x - 1] < 0:
                    possible_fields.append((x - 1, y - 1))
                if piece_board[y - 1, x - 1] > 0:
                    protected_fields.append((x - 1, y - 1))
            if x + 1 <= 7 and y - 1 >= 0:
                if piece_board[y - 1, x + 1] < 0:
                    possible_fields.append((x + 1, y - 1))
                if piece_board[y - 1, x + 1] > 0:
                    protected_fields.append((x + 1, y - 1))
        else:
            if x - 1 >= 0 and y + 1 <= 7:
                if piece_board[y + 1, x - 1] > 0:
                    possible_fields.append((x - 1, y + 1))
                if piece_board[y + 1, x - 1] < 0:
                    protected_fields.append((x - 1, y + 1))

            if x + 1 <= 7 and y + 1 <= 7:
                if piece_board[y + 1, x + 1] > 0:
                    possible_fields.append((x + 1, y + 1))
                if piece_board[y + 1, x + 1] < 0:
                    protected_fields.append((x + 1, y + 1))

        return possible_fields, protected_fields


    def get_attacked_fields(self) ->[Tuple[int, int]]:

        attacked_locations = []
        x = self.x
        y = self.y
        color = self.color

        if color == ColorEnum.WHITE:
            if x - 1 >= 0 and y - 1 >= 0:
                if x - 1 >= 0 and y - 1 >= 0:
                    attacked_locations.append((x - 1, y - 1))
            if x + 1 <= 7 and y - 1 >= 0:
                if x + 1 <= 7 and y - 1 >= 0:
                    attacked_locations.append((x + 1, y - 1))
        else:
            if x - 1 >= 0 and y + 1 <= 7:
                if x - 1 >= 0 and y + 1 <= 7:
                    attacked_locations.append((x - 1, y + 1))
            if x + 1 <= 7 and y + 1 <= 7:
                if x + 1 <= 7 and y + 1 <= 7:
                    attacked_locations.append((x + 1, y + 1))

        return attacked_locations

    @property
    def is_en_passant(self) -> bool:
        return self._is_en_passant

    @is_en_passant.setter
    def is_en_passant(self, value: bool) -> None:
        self._is_en_passant = value


    # @override
    # def get_possible_moves(self, board: Board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    #     possible_fields = []
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
    #     if color == ColorEnum.WHITE:
    #         if board.is_empty(x, y - 1):
    #             possible_fields.append((x, y - 1))
    #     else:
    #         if board.is_empty(x, y + 1):
    #             possible_fields.append((x, y + 1))
    #
    #     # Move two squares forward
    #     if not self.is_moved():
    #         if color == ColorEnum.WHITE:
    #             if board.is_empty(x, y - 1) and board.is_empty(x, y - 2):
    #                 possible_fields.append((x, y - 2))
    #         else:
    #             if board.is_empty(x, y + 1) and board.is_empty(x, y + 2):
    #                 possible_fields.append((x, y + 2))
    #
    #     # Capture diagonally
    #     if color == ColorEnum.WHITE:
    #         if board.is_enemy(x - 1, y - 1, color):
    #             possible_fields.append((x - 1, y - 1))
    #         if board.is_enemy(x + 1, y - 1, color):
    #             possible_fields.append((x + 1, y - 1))
    #     else:
    #         if board.is_enemy(x - 1, y + 1, color):
    #             possible_fields.append((x - 1, y + 1))
    #         if board.is_enemy(x + 1, y + 1, color):
    #             possible_fields.append((x + 1, y + 1))
    #
    #     # Remove moves that are out of bounds
    #     for move in possible_fields:
    #         if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:
    #             possible_fields.remove(move)
    #
    #     # Collect protected fields (fields that are protected by other pieces of the same color)
    #     if color == ColorEnum.WHITE:
    #         if board.is_friend(x - 1, y - 1, color):
    #             protected_fields.append((x - 1, y - 1))
    #         if board.is_friend(x + 1, y - 1, color):
    #             protected_fields.append((x + 1, y - 1))
    #     else:
    #         if board.is_friend(x - 1, y + 1, color):
    #             protected_fields.append((x - 1, y + 1))
    #         if board.is_friend(x + 1, y + 1, color):
    #             protected_fields.append((x + 1, y + 1))
    #
    #     return possible_fields, protected_fields