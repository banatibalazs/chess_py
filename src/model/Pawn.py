from typing import List, Tuple, override
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Pawn(Piece):
    def __init__(self, color: ColorEnum, x: int, y: int):
        super().__init__(PieceTypeEnum.PAWN, color, x, y)
        self._is_en_passant = False

    @override
    def update_piece(self, board: Board):
        self._possible_fields.clear()
        self._protected_fields.clear()
        x = self.x
        y = self.y
        color = self.color

        piece_board = board.get_piece_board()

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
                if piece_board[y - 1, x - 1] > 0:
                    self._protected_fields.add((x - 1, y - 1))
            if x + 1 <= 7 and y - 1 >= 0:
                if piece_board[y - 1, x + 1] < 0:
                    self._possible_fields.add((x + 1, y - 1))
                if piece_board[y - 1, x + 1] > 0:
                    self._protected_fields.add((x + 1, y - 1))
        else:
            if x - 1 >= 0 and y + 1 <= 7:
                if piece_board[y + 1, x - 1] > 0:
                    self._possible_fields.add((x - 1, y + 1))
                if piece_board[y + 1, x - 1] < 0:
                    self._protected_fields.add((x - 1, y + 1))

            if x + 1 <= 7 and y + 1 <= 7:
                if piece_board[y + 1, x + 1] > 0:
                    self._possible_fields.add((x + 1, y + 1))
                if piece_board[y + 1, x + 1] < 0:
                    self._protected_fields.add((x + 1, y + 1))


    def get_attacked_fields(self) ->[Tuple[int, int]]:

        attacked_locations = []
        x = self.x
        y = self.y
        color = self.color

        if color == ColorEnum.WHITE:
            if x - 1 >= 0 and y - 1 >= 0:
                if x - 1 >= 0 and y - 1 >= 0:
                    attacked_locations.append((x - 1, y - 1))
            if x + 1 <= 7 and y - 1 >= 0:
                if x + 1 <= 7 and y - 1 >= 0:
                    attacked_locations.append((x + 1, y - 1))
        else:
            if x - 1 >= 0 and y + 1 <= 7:
                if x - 1 >= 0 and y + 1 <= 7:
                    attacked_locations.append((x - 1, y + 1))
            if x + 1 <= 7 and y + 1 <= 7:
                if x + 1 <= 7 and y + 1 <= 7:
                    attacked_locations.append((x + 1, y + 1))

        return attacked_locations

    @property
    def is_en_passant(self) -> bool:
        return self._is_en_passant

    @is_en_passant.setter
    def is_en_passant(self, value: bool) -> None:
        self._is_en_passant = value

