from typing import override, List, Tuple

import src.model.Board as Board
from src.controller.CustomTypesForTypeHinting import ByteArray8x8
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.ROOK, color, x, y)

    # @override
    # def get_possible_moves(self, board: Board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:  # type: ignore
    #     possible_fields = []
    #     protected_fields = []
    #
    #     x = self.x
    #     y = self.y
    #     color = self.color
    #
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

    @override
    def get_possible_moves(self, board: Board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:  # type: ignore
        possible_fields = []
        protected_fields = []
        x = self.x
        y = self.y
        color = self.color

        board: ByteArray8x8 = board.get_piece_board()

        vectors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
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