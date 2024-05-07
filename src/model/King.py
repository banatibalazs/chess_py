from typing import override
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(PieceTypeEnum.KING, color, row, col)

    @override
    def update_attacked_fields(self, current_player, opponent):
        self._attacked_fields.clear()
        col = self.col
        row = self.row

        move_pattern_list = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col),
                             (row - 1, col - 1), (row + 1, col - 1), (row - 1, col + 1), (row + 1, col + 1)]

        for move in move_pattern_list:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                if opponent.has_piece_at(move[0], move[1]):
                    self._attacked_fields.add(move)
                elif current_player.has_piece_at(move[0], move[1]):
                    pass
                else:
                    self._attacked_fields.add(move)

    @override
    def update_possible_fields(self, current_player, opponent) -> None:
        self._possible_fields.clear()
        col = self.col
        row = self.row

        opponent_attacked_fields = set()
        for piece in opponent._pieces:
            for field in piece._attacked_fields:
                opponent_attacked_fields.add(field)

        for move in self._attacked_fields:
            if move not in opponent_attacked_fields:
                self._possible_fields.add(move)