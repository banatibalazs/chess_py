from typing import override
from src.model.pieces.Piece import Piece
from src.model.enums.PieceType import PieceType


class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__(PieceType.BISHOP, color, row, col)

    @override
    def update_attacked_fields(self, current_player, opponent):
        self._attacked_fields.clear()
        row = self.row
        col = self.col

        #          (row, col)
        vectors = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        directions = []
        for vector in vectors:
            direction = []
            for i in range(1, 8):
                if row + vector[0] * i > 7 or row + vector[0] * i < 0 or col + vector[1] * i > 7 or\
                        col + vector[1] * i < 0:
                    break
                direction.append((row + vector[0] * i, col + vector[1] * i))
            directions.append(direction)

        for direction in directions:
            for field in direction:
                row = field[0]
                col = field[1]
                if opponent.has_piece_at(row, col):
                    self._attacked_fields.add(field)
                    break
                elif current_player.has_piece_at(row, col):
                    break
                else:
                    self._attacked_fields.add(field)



