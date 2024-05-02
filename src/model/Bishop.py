from typing import override
from src.model.Piece import Piece
import src.model.Board as Board
from src.model.ColorEnum import ColorEnum
from src.model.PieceTypeEnum import PieceTypeEnum


class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.BISHOP, color, x, y)

    @override
    def update_attacked_fields(self, board: Board):
        self._attacked_fields.clear()
        x = self.x
        y = self.y
        color = self.color

        piece_board = board.get_piece_board()

        vectors = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        directions = []
        for vector in vectors:
            direction = []
            for i in range(1, 8):
                if x + vector[0] * i > 7 or x + vector[0] * i < 0 or y + vector[1] * i > 7 or y + vector[1] * i < 0:
                    break
                direction.append((x + vector[0] * i, y + vector[1] * i))
            directions.append(direction)

        for direction in directions:
            for field in direction:
                if color == ColorEnum.WHITE:
                    if piece_board[field[1], field[0]] == ColorEnum.NONE.value:
                        self._attacked_fields.add(field)
                    else:
                        self._attacked_fields.add(field)
                        break
                else:
                    if piece_board[field[1], field[0]] == 0:
                        self._attacked_fields.add(field)
                    else:
                        self._attacked_fields.add(field)
                        break
