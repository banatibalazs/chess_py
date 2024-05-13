from typing import override
from src.model.Color import Color
from src.model.Piece import Piece
from src.model.PieceType import PieceType


class Knight(Piece):
    def __init__(self, color: Color, row: int, col: int):
        super().__init__(PieceType.KNIGHT, color, row, col)

    @override
    def update_attacked_fields(self, current_player, opponent):
        self._attacked_fields.clear()
        col = self.col
        row = self.row

        move_pattern_list = [(row - 2, col - 1), (row - 2, col + 1), (row - 1, col - 2), (row - 1, col + 2),
                             (row + 1, col - 2), (row + 1, col + 2), (row + 2, col - 1), (row + 2, col + 1)]

        for move in move_pattern_list:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                if opponent.has_piece_at(move[0], move[1]):
                    self._attacked_fields.add(move)
                elif current_player.has_piece_at(move[0], move[1]):
                    pass
                else:
                    self._attacked_fields.add(move)


