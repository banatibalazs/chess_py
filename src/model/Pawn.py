from typing import List, Tuple, override, Set

from src.controller.CustomTypesForTypeHinting import ByteArray8x8
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Pawn(Piece):
    def __init__(self, color: ColorEnum, x: int, y: int):
        super().__init__(PieceTypeEnum.PAWN, color, x, y)
        self._is_en_passant = False

    @override
    def update_attacked_fields(self, piece_board: ByteArray8x8):
        self._attacked_fields.clear()
        x = self.x
        y = self.y
        color = self.color

        if color == ColorEnum.WHITE:
            if x - 1 >= 0 and y - 1 >= 0:
                if x - 1 >= 0 and y - 1 >= 0:
                    self._attacked_fields.add((x - 1, y - 1))
            if x + 1 <= 7 and y - 1 >= 0:
                if x + 1 <= 7 and y - 1 >= 0:
                    self._attacked_fields.add((x + 1, y - 1))
        else:
            if x - 1 >= 0 and y + 1 <= 7:
                if x - 1 >= 0 and y + 1 <= 7:
                    self._attacked_fields.add((x - 1, y + 1))
            if x + 1 <= 7 and y + 1 <= 7:
                if x + 1 <= 7 and y + 1 <= 7:
                    self._attacked_fields.add((x + 1, y + 1))

        self.update_protected_fields(piece_board)


    @override
    def update_possible_fields(self, piece_board: ByteArray8x8, opponent_pieces) -> None:
        self._possible_fields.clear()
        x = self.x
        y = self.y
        color = self.color

        # Move forward
        if color == ColorEnum.WHITE:
            if y - 1 >= 0:
                if piece_board[y - 1, x] == 0:
                    self._possible_fields.add((x, y - 1))
        else:
            if y + 1 <= 7:
                if piece_board[y + 1, x] == 0:
                    self._possible_fields.add((x, y + 1))

        # Move two squares forward
        if color == ColorEnum.WHITE and y == 6:
            if piece_board[y - 1, x] == 0 and piece_board[y - 2, x] == 0:
                self._possible_fields.add((x, y - 2))
        elif color == ColorEnum.BLACK and y == 1:
            if piece_board[y + 1, x] == 0 and piece_board[y + 2, x] == 0:
                self._possible_fields.add((x, y + 2))

        # Diagonal capture
        if color == ColorEnum.WHITE:
            if x - 1 >= 0 and y - 1 >= 0:
                if piece_board[y - 1, x - 1] < 0:
                    self._possible_fields.add((x - 1, y - 1))
            if x + 1 <= 7 and y - 1 >= 0:
                if piece_board[y - 1, x + 1] < 0:
                    self._possible_fields.add((x + 1, y - 1))
        else:
            if x - 1 >= 0 and y + 1 <= 7:
                if piece_board[y + 1, x - 1] > 0:
                    self._possible_fields.add((x - 1, y + 1))

            if x + 1 <= 7 and y + 1 <= 7:
                if piece_board[y + 1, x + 1] > 0:
                    self._possible_fields.add((x + 1, y + 1))



    @property
    def is_en_passant(self) -> bool:
        return self._is_en_passant

    @is_en_passant.setter
    def is_en_passant(self, value: bool) -> None:
        self._is_en_passant = value

    @override
    @property
    def attacked_fields(self) -> Set[Tuple[int, int]]:
        return self._attacked_fields

