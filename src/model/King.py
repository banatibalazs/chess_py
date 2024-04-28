from typing import override

from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.KING, color, x, y)

    @override
    def get_possible_moves(self, board) -> object:
        possible_moves = []
        x = self.x
        y = self.y
        color = self.color

        if board.is_empty(x, y - 1) or board.is_enemy(x, y - 1, color):
            possible_moves.append((x, y - 1))
        if board.is_empty(x, y + 1) or board.is_enemy(x, y + 1, color):
            possible_moves.append((x, y + 1))
        if board.is_empty(x - 1, y) or board.is_enemy(x - 1, y, color):
            possible_moves.append((x - 1, y))
        if board.is_empty(x + 1, y) or board.is_enemy(x + 1, y, color):
            possible_moves.append((x + 1, y))
        if board.is_empty(x - 1, y - 1) or board.is_enemy(x - 1, y - 1, color):
            possible_moves.append((x - 1, y - 1))
        if board.is_empty(x + 1, y - 1) or board.is_enemy(x + 1, y - 1, color):
            possible_moves.append((x + 1, y - 1))
        if board.is_empty(x - 1, y + 1) or board.is_enemy(x - 1, y + 1, color):
            possible_moves.append((x - 1, y + 1))
        if board.is_empty(x + 1, y + 1) or board.is_enemy(x + 1, y + 1, color):
            possible_moves.append((x + 1, y + 1))


        for move in possible_moves:
            if color == ColorEnum.WHITE:
                if board.square_is_attacked_by_black(move[0], move[1]):
                    possible_moves.remove(move)
            else:
                if board.square_is_attacked_by_white(move[0], move[1]):
                    possible_moves.remove(move)


        return possible_moves