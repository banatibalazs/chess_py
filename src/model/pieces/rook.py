from typing import override, Set, Tuple
from src.model.pieces.piece import Piece
from src.model.enums.enums import PieceType


class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(PieceType.ROOK, color, row, col)

    @override
    def update_attacked_fields(self, current_player_piece_coordinates: Set[Tuple[int, int]],
                               opponent_piece_coordinates: Set[Tuple[int, int]]) -> None:
        self._attacked_fields.clear()
        col = self.col
        row = self.row

        vectors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        directions = [
            [(row + vector[0] * i, col + vector[1] * i) for i in range(1, 8)
             if 0 <= row + vector[0] * i <= 7 and 0 <= col + vector[1] * i <= 7]
            for vector in vectors
        ]

        for direction in directions:
            for field in direction:
                if field in opponent_piece_coordinates:
                    self._attacked_fields.add(field)
                    break
                elif field in current_player_piece_coordinates:
                    break
                else:
                    self._attacked_fields.add(field)
