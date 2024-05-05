from typing import Tuple, override, Set
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Pawn(Piece):
    def __init__(self, color: ColorEnum, row: int, col: int):
        super().__init__(PieceTypeEnum.PAWN, color, row, col)
        self._is_en_passant = False

    @override
    def update_attacked_fields(self, current_player, opponent):
        self._attacked_fields.clear()
        col = self.col
        row = self.row
        color = self.color

        if color == ColorEnum.WHITE:
            if col - 1 >= 0 and row - 1 >= 0:
                if current_player.has_piece_at(row - 1, col - 1):
                    pass
                else:
                    self._attacked_fields.add((row - 1, col - 1))

            if col + 1 <= 7 and row - 1 >= 0:
                if current_player.has_piece_at(row - 1, col + 1):
                    pass
                else:
                    self._attacked_fields.add((row - 1, col + 1))
        else:
            if col - 1 >= 0 and row + 1 <= 7:
                if current_player.has_piece_at(row + 1, col - 1):
                    pass
                else:
                    self._attacked_fields.add((row + 1, col - 1))
            if col + 1 <= 7 and row + 1 <= 7:
                if current_player.has_piece_at(row + 1, col + 1):
                    pass
                else:
                    self._attacked_fields.add((row + 1, col + 1))




    @override
    def update_possible_fields(self, current_player, opponent) -> None:
        self._possible_fields.clear()
        col = self.col
        row = self.row
        color = self.color

        piece_board = current_player._board.get_piece_board()

        # Move forward
        if color == ColorEnum.WHITE:
            if row - 1 >= 0:
                if piece_board[row - 1, col] == 0:
                    self._possible_fields.add((row - 1, col))
        else:
            if row + 1 <= 7:
                if piece_board[row + 1, col] == 0:
                    self._possible_fields.add((row + 1, col))

        # Move two squares forward
        if color == ColorEnum.WHITE and row == 6:
            if piece_board[row - 1, col] == 0 and piece_board[row - 2, col] == 0:
                self._possible_fields.add((row - 2, col))
        elif color == ColorEnum.BLACK and row == 1:
            if piece_board[row + 1, col] == 0 and piece_board[row + 2, col] == 0:
                self._possible_fields.add((row + 2, col))

        # Diagonal capture
        if color == ColorEnum.WHITE:
            if col - 1 >= 0 and row - 1 >= 0:
                if piece_board[row - 1, col - 1] < 0:
                    self._possible_fields.add((row - 1, col - 1))
            if col + 1 <= 7 and row - 1 >= 0:
                if piece_board[row - 1, col + 1] < 0:
                    self._possible_fields.add((row - 1, col + 1))
        else:
            if col - 1 >= 0 and row + 1 <= 7:
                if piece_board[row + 1, col - 1] > 0:
                    self._possible_fields.add((row + 1, col - 1))

            if col + 1 <= 7 and row + 1 <= 7:
                if piece_board[row + 1, col + 1] > 0:
                    self._possible_fields.add((row + 1, col + 1))



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

