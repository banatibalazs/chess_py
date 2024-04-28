from typing import override

from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.ROOK, color, x, y)

    @override
    def get_possible_moves(self, board):
        possible_moves = []

        x = self.x
        y = self.y
        color = self.color

        for i in range(1, 8):
            if x + i > 7:
                break
            if board.is_empty(x + i, y):
                possible_moves.append((x + i, y))
            elif board.is_enemy(x + i, y, color):
                possible_moves.append((x + i, y))
                break
            else:
                break

        for i in range(1, 8):
            if x - i < 0:
                break
            if board.is_empty(x - i, y):
                possible_moves.append((x - i, y))
            elif board.is_enemy(x - i, y, color):
                possible_moves.append((x - i, y))
                break
            else:
                break

        for i in range(1, 8):
            if y + i > 7:
                break
            if board.is_empty(x, y + i):
                possible_moves.append((x, y + i))
            elif board.is_enemy(x, y + i, color):
                possible_moves.append((x, y + i))
                break
            else:
                break

        for i in range(1, 8):
            if y - i < 0:
                break
            if board.is_empty(x, y - i):
                possible_moves.append((x, y - i))
            elif board.is_enemy(x, y - i, color):
                possible_moves.append((x, y - i))
                break
            else:
                break

        return possible_moves
