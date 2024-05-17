from typing import override, Tuple, Set
from src.model.enums.Color import Color
from src.model.pieces.Piece import Piece
from src.model.enums.PieceType import PieceType


class Knight(Piece):
    def __init__(self, color: Color, row: int, col: int):
        super().__init__(PieceType.KNIGHT, color, row, col)

    @override
    def update_attacked_fields(self, current_player_piece_coordinates: Set[Tuple[int, int]],
                               opponent_piece_coordinates: Set[Tuple[int, int]]) -> None:
        self._attacked_fields.clear()
        col = self.col
        row = self.row

        move_pattern_list = [(row - 2, col - 1), (row - 2, col + 1), (row - 1, col - 2), (row - 1, col + 2),
                             (row + 1, col - 2), (row + 1, col + 2), (row + 2, col - 1), (row + 2, col + 1)]

        for move in move_pattern_list:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                if move in opponent_piece_coordinates:
                    self._attacked_fields.add(move)
                elif move in current_player_piece_coordinates:
                    pass
                else:
                    self._attacked_fields.add(move)


