from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.KING, color, x, y)

    def get_possible_moves(self, board):
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


        return possible_moves