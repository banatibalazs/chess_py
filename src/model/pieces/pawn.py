from typing import Tuple, override, Set
from src.model.enums.enums import Color
from src.model.pieces.piece import Piece
from src.model.enums.enums import PieceType


class Pawn(Piece):
    def __init__(self, color: Color, row: int, col: int) -> None:
        super().__init__(PieceType.PAWN, color, row, col)
        self._is_en_passant = False

    @override
    def update_attacked_fields(self, current_player_piece_coordinates: Set[Tuple[int, int]],
                               opponent_piece_coordinates: Set[Tuple[int, int]]) -> None:
        self._attacked_fields.clear()
        col = self.col
        row = self.row
        color = self.color

        if color == Color.W:
            if col - 1 >= 0 and row - 1 >= 0:
                if (row - 1, col - 1) in current_player_piece_coordinates:
                    pass
                else:
                    self._attacked_fields.add((row - 1, col - 1))

            if col + 1 <= 7 and row - 1 >= 0:
                if (row - 1, col + 1) in current_player_piece_coordinates:
                    pass
                else:
                    self._attacked_fields.add((row - 1, col + 1))
        else:
            if col - 1 >= 0 and row + 1 <= 7:
                if (row + 1, col - 1) in current_player_piece_coordinates:
                    pass
                else:
                    self._attacked_fields.add((row + 1, col - 1))
            if col + 1 <= 7 and row + 1 <= 7:
                if (row + 1, col + 1) in current_player_piece_coordinates:
                    pass
                else:
                    self._attacked_fields.add((row + 1, col + 1))

    @override
    def update_possible_fields(self, white_piece_coordinates, black_piece_coordinates, board) -> None:
        self._possible_fields.clear()
        possible_fields = set()

        col = self.col
        row = self.row
        color = self.color

        # Move forward
        if color == Color.W:
            if row - 1 >= 0:
                if board[row - 1, col] == 0:
                    possible_fields.add((row - 1, col))
        else:
            if row + 1 <= 7:
                if board[row + 1, col] == 0:
                    possible_fields.add((row + 1, col))

        # Move two squares forward
        if color == Color.W and row == 6:
            if board[row - 1, col] == 0 and board[row - 2, col] == 0:
                possible_fields.add((row - 2, col))
        elif color == Color.B and row == 1:
            if board[row + 1, col] == 0 and board[row + 2, col] == 0:
                possible_fields.add((row + 2, col))

        # Diagonal capture
        if color == Color.W:
            if col - 1 >= 0 and row - 1 >= 0:
                if (row - 1, col - 1) in black_piece_coordinates:
                    possible_fields.add((row - 1, col - 1))
            if col + 1 <= 7 and row - 1 >= 0:
                if (row - 1, col + 1) in black_piece_coordinates:
                    possible_fields.add((row - 1, col + 1))
        else:
            if col - 1 >= 0 and row + 1 <= 7:
                if (row + 1, col - 1) in white_piece_coordinates:
                    possible_fields.add((row + 1, col - 1))

            if col + 1 <= 7 and row + 1 <= 7:
                if (row + 1, col + 1) in white_piece_coordinates:
                    possible_fields.add((row + 1, col + 1))

        self._possible_fields = possible_fields

        # # Add en passant if possible
        # if opponent._last_moved_piece is not None and \
        #         isinstance(opponent._last_moved_piece, Pawn) and \
        #         opponent._last_moved_piece.is_en_passant and \
        #         self.row == opponent._last_moved_piece.row and \
        #         abs(self.col - opponent._last_moved_piece.col) == 1:
        #     # print("En passant move is added.")
        #     if self._color == Color.W:
        #         possible_fields.add((opponent._last_moved_piece.row - 1, opponent._last_moved_piece.col))
        #     else:
        #         possible_fields.add((opponent._last_moved_piece.row + 1, opponent._last_moved_piece.col))

        # # Check if the move is valid
        # opponent_attacked_fields = set()
        # for piece in opponent._pieces:
        #     for field in piece._attacked_fields:
        #         opponent_attacked_fields.add(field)

        # for move in possible_fields:
        #     if not self.king_in_check_after_move(move, current_player, opponent):
        #         self._possible_fields.add(move)

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
