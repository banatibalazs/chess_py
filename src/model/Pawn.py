from typing import Tuple, override, Set
from src.model.Color import Color
from src.model.Piece import Piece
from src.model.PieceType import PieceType


class Pawn(Piece):
    def __init__(self, color: Color, row: int, col: int) -> None:
        super().__init__(PieceType.PAWN, color, row, col)
        self._is_en_passant = False

    @override
    def update_attacked_fields(self, current_player, opponent) -> None:
        self._attacked_fields.clear()
        col = self.col
        row = self.row
        color = self.color

        if color == Color.WHITE:
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
        possible_fields = set()

        col = self.col
        row = self.row
        color = self.color

        # Move forward
        if color == Color.WHITE:
            if row - 1 >= 0:
                if not opponent.has_piece_at(row - 1, col) and not current_player.has_piece_at(row - 1, col):
                    possible_fields.add((row - 1, col))
        else:
            if row + 1 <= 7:
                if not opponent.has_piece_at(row + 1, col) and not current_player.has_piece_at(row + 1, col):
                    possible_fields.add((row + 1, col))

        # Move two squares forward
        if color == Color.WHITE and row == 6:
            if (not opponent.has_piece_at(row - 1, col) and not current_player.has_piece_at(row - 1, col) and
                    not opponent.has_piece_at(row - 2, col) and not current_player.has_piece_at(row - 2, col)):
                possible_fields.add((row - 2, col))
        elif color == Color.BLACK and row == 1:
            if (not opponent.has_piece_at(row + 1, col) and not current_player.has_piece_at(row + 1, col) and
             not opponent.has_piece_at(row + 2, col) and not current_player.has_piece_at(row + 2, col)):
                possible_fields.add((row + 2, col))

        # Diagonal capture
        if color == Color.WHITE:
            if col - 1 >= 0 and row - 1 >= 0:
                if opponent.has_piece_at(row - 1, col - 1):
                    possible_fields.add((row - 1, col - 1))
            if col + 1 <= 7 and row - 1 >= 0:
                if opponent.has_piece_at(row - 1, col + 1):
                    possible_fields.add((row - 1, col + 1))
        else:
            if col - 1 >= 0 and row + 1 <= 7:
                if opponent.has_piece_at(row + 1, col - 1):
                    possible_fields.add((row + 1, col - 1))

            if col + 1 <= 7 and row + 1 <= 7:
                if opponent.has_piece_at(row + 1, col + 1):
                    possible_fields.add((row + 1, col + 1))

        # Add en passant if possible
        if opponent._last_moved_piece is not None and \
                isinstance(opponent._last_moved_piece, Pawn) and \
                opponent._last_moved_piece.is_en_passant and \
                self.row == opponent._last_moved_piece.row and \
                abs(self.col - opponent._last_moved_piece.col) == 1:
            if self._color == Color.WHITE:
                print("En passant move is added.")
                possible_fields.add((opponent._last_moved_piece.row - 1, opponent._last_moved_piece.col))
            else:
                possible_fields.add((opponent._last_moved_piece.row + 1, opponent._last_moved_piece.col))

        # Check if the move is valid
        opponent_attacked_fields = set()
        for piece in opponent._pieces:
            for field in piece._attacked_fields:
                opponent_attacked_fields.add(field)

        for move in possible_fields:
            if not self.king_in_check_after_move(move, current_player, opponent):
                self._possible_fields.add(move)

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
