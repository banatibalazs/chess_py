from typing import override, Tuple, List
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum
import src.model.Board as Board


class Queen(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.QUEEN, color, x, y)

    @override
    def update_piece(self, board: Board):
        self._possible_fields.clear()
        self._protected_fields.clear()
        x = self.x
        y = self.y
        color = self.color

        piece_board = board.get_piece_board()

        vectors = [(1, 0), (-1, 0), (0, 1), (0, -1),
                   (1, 1), (-1, 1), (1, -1), (-1, -1)]
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
                    if piece_board[field[1], field[0]] == 0:
                        self._possible_fields.add(field)
                    elif piece_board[field[1], field[0]] < 0:
                        self._possible_fields.add(field)
                        break
                    else:
                        self._protected_fields.add(field)
                        break
                else:
                    if piece_board[field[1], field[0]] == 0:
                        self._possible_fields.add(field)
                    elif piece_board[field[1], field[0]] > 0:
                        self._possible_fields.add(field)
                        break
                    else:
                        self._protected_fields.add(field)
                        break
