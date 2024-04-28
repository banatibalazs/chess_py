from typing import override, Tuple, List
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.BISHOP, color, x, y)

    @override
    def get_possible_moves(self, board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        possible_moves = []
        protected_fields = []
        x = self.x
        y = self.y
        color = self.color

        for i in range(1, 8):
            if board.is_empty(x + i, y + i):
                possible_moves.append((x + i, y + i))
            elif board.is_enemy(x + i, y + i, color):
                possible_moves.append((x + i, y + i))
                break
            elif board.is_friend(x + i, y + i, color):
                protected_fields.append((x + i, y + i))
                break
            else:
                break

        for i in range(1, 8):
            if board.is_empty(x - i, y + i):
                possible_moves.append((x - i, y + i))
            elif board.is_enemy(x - i, y + i, color):
                possible_moves.append((x - i, y + i))
                break
            elif board.is_friend(x - i, y + i, color):
                protected_fields.append((x - i, y + i))
                break
            else:
                break

        for i in range(1, 8):
            if board.is_empty(x + i, y - i):
                possible_moves.append((x + i, y - i))
            elif board.is_enemy(x + i, y - i, color):
                possible_moves.append((x + i, y - i))
                break
            elif board.is_friend(x + i, y - i, color):
                protected_fields.append((x + i, y - i))
                break
            else:
                break

        for i in range(1, 8):
            if board.is_empty(x - i, y - i):
                possible_moves.append((x - i, y - i))
            elif board.is_enemy(x - i, y - i, color):
                possible_moves.append((x - i, y - i))
                break
            elif board.is_friend(x - i, y - i, color):
                protected_fields.append((x - i, y - i))
                break
            else:
                break

        return possible_moves, protected_fields
