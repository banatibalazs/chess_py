from typing import override, Tuple, List

from src.controller.CustomTypesForTypeHinting import ByteArray8x8
import src.model.Board as Board
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Queen(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.QUEEN, color, x, y)

    @override
    def get_possible_moves(self, board: Board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        possible_fields = []
        protected_fields = []
        x = self.x
        y = self.y
        color = self.color

        board: ByteArray8x8 = board.get_piece_board()

        vectors = [(1, 0), (-1, 0), (0, 1), (0, -1),
                   (1, 1), (-1, 1), (1, -1), (-1, -1)]
        directions = []
        for vector in vectors:
            direction = []
            for i in range(1, 8):
                if x + vector[0] * i > 7 or x + vector[0] * i < 0 or y + vector[1] * i > 7 or y + vector[1] * i < 0:
                    break
                direction.append((x + vector[0] * i, y + vector[1] * i))
            directions.append(direction)

        for direction in directions:
            for field in direction:
                if color == ColorEnum.WHITE:
                    if board[field[1], field[0]] == 0:
                        possible_fields.append(field)
                    elif board[field[1], field[0]] > 0:
                        protected_fields.append(field)
                        break
                    elif board[field[1], field[0]] < 0:
                        possible_fields.append(field)
                        break
                else:
                    if board[field[1], field[0]] == 0:
                        possible_fields.append(field)
                    elif board[field[1], field[0]] < 0:
                        protected_fields.append(field)
                        break
                    elif board[field[1], field[0]] > 0:
                        possible_fields.append(field)
                        break

        return possible_fields, protected_fields

    # @override
    # def get_possible_moves(self, board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    #     possible_fields = []
    #     protected_fields = []
    #
    #     x = self.x
    #     y = self.y
    #     color = self.color
    #
    #     '''
    #     The board
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
    #     # Move diagonally
    #     for i in range(1, 8):
    #         if x + i > 7 or y + i > 7:
    #             break
    #         if board.is_empty(x + i, y + i):
    #             possible_fields.append((x + i, y + i))
    #         elif board.is_enemy(x + i, y + i, color):
    #             possible_fields.append((x + i, y + i))
    #             break
    #         elif board.is_friend(x + i, y + i, color):
    #             protected_fields.append((x + i, y + i))
    #             break
    #         else:
    #             break
    #
    #     for i in range(1, 8):
    #         if x - i < 0 or y + i > 7:
    #             break
    #         if board.is_empty(x - i, y + i):
    #             possible_fields.append((x - i, y + i))
    #         elif board.is_enemy(x - i, y + i, color):
    #             possible_fields.append((x - i, y + i))
    #             break
    #         elif board.is_friend(x - i, y + i, color):
    #             protected_fields.append((x - i, y + i))
    #             break
    #         else:
    #             break
    #
    #     for i in range(1, 8):
    #         if x + i > 7 or y - i < 0:
    #             break
    #         if board.is_empty(x + i, y - i):
    #             possible_fields.append((x + i, y - i))
    #         elif board.is_enemy(x + i, y - i, color):
    #             possible_fields.append((x + i, y - i))
    #             break
    #         elif board.is_friend(x + i, y - i, color):
    #             protected_fields.append((x + i, y - i))
    #             break
    #         else:
    #             break
    #
    #     for i in range(1, 8):
    #         if x - i < 0 or y - i < 0:
    #             break
    #         if board.is_empty(x - i, y - i):
    #             possible_fields.append((x - i, y - i))
    #         elif board.is_enemy(x - i, y - i, color):
    #             possible_fields.append((x - i, y - i))
    #             break
    #         elif board.is_friend(x - i, y - i, color):
    #             protected_fields.append((x - i, y - i))
    #             break
    #         else:
    #             break
    #
    #     # Move horizontally
    #     for i in range(1, 8):
    #         if x + i > 7:
    #             break
    #         if board.is_empty(x + i, y):
    #             possible_fields.append((x + i, y))
    #         elif board.is_enemy(x + i, y, color):
    #             possible_fields.append((x + i, y))
    #             break
    #         elif board.is_friend(x + i, y, color):
    #             protected_fields.append((x + i, y))
    #             break
    #         else:
    #             break
    #
    #     for i in range(1, 8):
    #         if x - i < 0:
    #             break
    #         if board.is_empty(x - i, y):
    #             possible_fields.append((x - i, y))
    #         elif board.is_enemy(x - i, y, color):
    #             possible_fields.append((x - i, y))
    #             break
    #         elif board.is_friend(x - i, y, color):
    #             protected_fields.append((x - i, y))
    #             break
    #         else:
    #             break
    #
    #     # Move vertically
    #     for i in range(1, 8):
    #         if y + i > 7:
    #             break
    #         if board.is_empty(x, y + i):
    #             possible_fields.append((x, y + i))
    #         elif board.is_enemy(x, y + i, color):
    #             possible_fields.append((x, y + i))
    #             break
    #         elif board.is_friend(x, y + i, color):
    #             protected_fields.append((x, y + i))
    #             break
    #         else:
    #             break
    #
    #     for i in range(1, 8):
    #         if y - i < 0:
    #             break
    #         if board.is_empty(x, y - i):
    #             possible_fields.append((x, y - i))
    #         elif board.is_enemy(x, y - i, color):
    #             possible_fields.append((x, y - i))
    #             break
    #         elif board.is_friend(x, y - i, color):
    #             protected_fields.append((x, y - i))
    #             break
    #         else:
    #             break
    #
    #     return possible_fields, protected_fields