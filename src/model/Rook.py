from typing import override, List, Tuple

import src.model.Board as Board
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.ROOK, color, x, y)

    @override
    def get_possible_moves(self, board: Board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        possible_fields = []
        protected_fields = []

        x = self.x
        y = self.y
        color = self.color

        for i in range(1, 8):
            if x + i > 7:
                break
            if board.is_empty(x + i, y):
                possible_fields.append((x + i, y))
            elif board.is_enemy(x + i, y, color):
                possible_fields.append((x + i, y))
                break
            elif board.is_friend(x + i, y, color):
                protected_fields.append((x + i, y))
                break
            else:
                break

        for i in range(1, 8):
            if x - i < 0:
                break
            if board.is_empty(x - i, y):
                possible_fields.append((x - i, y))
            elif board.is_enemy(x - i, y, color):
                possible_fields.append((x - i, y))
                break
            elif board.is_friend(x - i, y, color):
                protected_fields.append((x - i, y))
                break
            else:
                break

        for i in range(1, 8):
            if y + i > 7:
                break
            if board.is_empty(x, y + i):
                possible_fields.append((x, y + i))
            elif board.is_enemy(x, y + i, color):
                possible_fields.append((x, y + i))
                break
            elif board.is_friend(x, y + i, color):
                protected_fields.append((x, y + i))
                break
            else:
                break

        for i in range(1, 8):
            if y - i < 0:
                break
            if board.is_empty(x, y - i):
                possible_fields.append((x, y - i))
            elif board.is_enemy(x, y - i, color):
                possible_fields.append((x, y - i))
                break
            elif board.is_friend(x, y - i, color):
                protected_fields.append((x, y - i))
                break
            else:
                break

        return possible_fields, protected_fields
