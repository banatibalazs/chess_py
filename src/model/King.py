import copy
from typing import override, Tuple, List

import numpy as np

from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.KING, color, x, y)

    @override
    def update_attacked_fields(self, board: Board):
        self._attacked_fields.clear()
        # self._protected_fields.clear()
        x = self.x
        y = self.y
        color = self.color

        move_pattern_list = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y),
                             (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]

        for move in move_pattern_list:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                self._attacked_fields.add(move)


    def update_protected_fields(self, board: Board):
        self._protected_fields.clear()
        for field in self._attacked_fields:
            if self._color == ColorEnum.WHITE:
                if board.get_piece(field[0], field[1]) > 0:
                    self._protected_fields.add(field)
            else:
                if board.get_piece(field[0], field[1]) < 0:
                    self._protected_fields.add(field)

    def check_if_king_is_attacked_after_move(self, board: Board, move: Tuple[int, int],
                                             opponent_pieces: List["Piece"]) -> bool:
        # Copy the board
        copy_piece_board = copy.deepcopy(board.get_piece_board())

        # Get the king position
        if self.color == ColorEnum.WHITE:
            own_king_y, own_king_x = np.where(copy_piece_board == 6)
        else:
            own_king_y, own_king_x = np.where(copy_piece_board == -6)

        # Moving piece data
        from_x, from_y = self.x, self.y
        to_x, to_y = move
        value = self._type.value
        color = self.color

        # Move the piece
        copy_piece_board[from_y, from_x] = 0
        copy_piece_board[to_y, to_x] = value if color == ColorEnum.WHITE else -value

        # Update update opponents attack fields
        for piece in opponent_pieces:
            piece.update_attacked_fields(copy_piece_board)

        return False

    def update_possible_fields(self, board: Board):
        self._possible_fields = self._attacked_fields - self._protected_fields
