from typing import override, Tuple, Set

from src.model.enums.enums import Color
from src.model.pieces.piece import Piece
from src.model.enums.enums import PieceType
from src.model.pieces.rook import Rook


class King(Piece):
    def __init__(self, color: Color, row: int, col: int) -> None:
        super().__init__(PieceType.KING, color, row, col)
        self._is_in_check = False

    @override
    def update_attacked_fields(self, current_player_piece_coordinates: Set[Tuple[int, int]],
                               opponent_piece_coordinates: Set[Tuple[int, int]], board) -> None:
        self._attacked_fields.clear()
        col = self.col
        row = self.row

        move_pattern_list = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col),
                             (row - 1, col - 1), (row + 1, col - 1), (row - 1, col + 1), (row + 1, col + 1)]

        for move in move_pattern_list:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                if move in opponent_piece_coordinates:
                    self._attacked_fields.add(move)
                elif move in current_player_piece_coordinates:
                    pass
                else:
                    self._attacked_fields.add(move)

    @override
    def update_possible_fields(self, current_player, opponent, board) -> None:
        self._possible_fields.clear()
        possible_fields = self._attacked_fields.copy()

        if (self.row, self.col) in opponent._attacked_fields:
            self._is_in_check = True
            print("King is in check")
        else:
            self._is_in_check = False

        # Add Castling moves
        def is_castling_possible(rook, cols):
            # TODO implement this with a Board, so that the check for empty fields would be more efficient
            return (isinstance(rook, Rook) and
                    not rook.is_moved and
                    not self.is_moved and
                    not self._is_in_check and
                    not any(current_player.has_piece_at(self.row, col) for col in cols) and
                    not any(opponent.has_piece_at(self.row, col) for col in cols) and
                    not any((self.row, col) in opponent._attacked_fields for col in cols))

        if self._color == Color.B:
            if is_castling_possible(current_player.get_piece_at(0, 0), range(1, 4)):
                possible_fields.add((0, 2))
            if is_castling_possible(current_player.get_piece_at(0, 7), range(5, 7)):
                possible_fields.add((0, 6))
        else:
            if is_castling_possible(current_player.get_piece_at(7, 0), range(1, 4)):
                possible_fields.add((7, 2))
            if is_castling_possible(current_player.get_piece_at(7, 7), range(5, 7)):
                possible_fields.add((7, 6))

        for move in possible_fields:
            if move not in opponent._attacked_fields and not self.king_in_check_after_move(move, current_player, opponent):
                self._possible_fields.add(move)

    @property
    def is_in_check(self) -> bool:
        return self._is_in_check


