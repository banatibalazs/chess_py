from typing import override
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Knight(Piece):
    def __init__(self, color: ColorEnum, x: int, y: int):
        super().__init__(PieceTypeEnum.KNIGHT, color, x, y)

    @override
    def update_piece(self, board: Board):
        self._possible_fields.clear()
        self._protected_fields.clear()
        x = self.x
        y = self.y
        color = self.color

        piece_board = board.get_piece_board()

        move_pattern_list = [(x - 1, y - 2), (x + 1, y - 2), (x - 2, y - 1), (x + 2, y - 1),
                             (x - 2, y + 1), (x + 2, y + 1), (x - 1, y + 2), (x + 1, y + 2)]

        for move in move_pattern_list:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:

                field = piece_board[move[1], move[0]]
                if color == ColorEnum.WHITE:
                    if field <= 0:
                        self._possible_fields.add(move)
                    else:
                        self._protected_fields.add(move)
                else:
                    if field >= 0:
                        self._possible_fields.add(move)
                    else:
                        self._protected_fields.add(move)
