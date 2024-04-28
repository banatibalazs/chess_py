from typing import override, Tuple, List

from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.KING, color, x, y)

    @override
    def get_possible_moves(self, board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        possible_fields = []
        protected_fields = []
        x = self.x
        y = self.y
        color = self.color

        # Move vertically
        if board.is_empty(x, y - 1) or board.is_enemy(x, y - 1, color):
            possible_fields.append((x, y - 1))
        elif board.is_friend(x, y - 1, color):
            protected_fields.append((x, y - 1))

        # Move vertically
        if board.is_empty(x, y + 1) or board.is_enemy(x, y + 1, color):
            possible_fields.append((x, y + 1))
        elif board.is_friend(x, y + 1, color):
            protected_fields.append((x, y + 1))

        # Move horizontally
        if board.is_empty(x - 1, y) or board.is_enemy(x - 1, y, color):
            possible_fields.append((x - 1, y))
        elif board.is_friend(x - 1, y, color):
            protected_fields.append((x - 1, y))

        # Move horizontally
        if board.is_empty(x + 1, y) or board.is_enemy(x + 1, y, color):
            possible_fields.append((x + 1, y))
        elif board.is_friend(x + 1, y, color):
            protected_fields.append((x + 1, y))

        # Move diagonally
        if board.is_empty(x - 1, y - 1) or board.is_enemy(x - 1, y - 1, color):
            possible_fields.append((x - 1, y - 1))
        elif board.is_friend(x - 1, y - 1, color):
            protected_fields.append((x - 1, y - 1))

        # Move diagonally
        if board.is_empty(x + 1, y - 1) or board.is_enemy(x + 1, y - 1, color):
            possible_fields.append((x + 1, y - 1))
        elif board.is_friend(x + 1, y - 1, color):
            protected_fields.append((x + 1, y - 1))

        # Move diagonally
        if board.is_empty(x - 1, y + 1) or board.is_enemy(x - 1, y + 1, color):
            possible_fields.append((x - 1, y + 1))
        elif board.is_friend(x - 1, y + 1, color):
            protected_fields.append((x - 1, y + 1))

        # Move diagonally
        if board.is_empty(x + 1, y + 1) or board.is_enemy(x + 1, y + 1, color):
            possible_fields.append((x + 1, y + 1))
        elif board.is_friend(x + 1, y + 1, color):
            protected_fields.append((x + 1, y + 1))

        for field in possible_fields:
            # if field in board._opponent_player.attacked_fields:
            #     possible_fields.remove(field)

            if color == ColorEnum.WHITE:
                if board.square_is_attacked_by_black(field[0], field[1]) or \
                        board.square_is_protected_by_black(field[0], field[1]):
                    possible_fields.remove(field)
            else:
                if board.square_is_attacked_by_white(field[0], field[1]) or \
                        board.square_is_protected_by_white(field[1], field[0]):
                    possible_fields.remove(field)


        return possible_fields, protected_fields
