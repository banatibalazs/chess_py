from typing import override

from src.model.enums.Color import Color
from src.model.pieces.Piece import Piece
from src.model.enums.PieceType import PieceType
from src.model.pieces.Rook import Rook


class King(Piece):
    def __init__(self, color: Color, row: int, col: int) -> None:
        super().__init__(PieceType.KING, color, row, col)
        self._is_in_check = False

    @override
    def update_attacked_fields(self, current_player, opponent):
        self._attacked_fields.clear()
        col = self.col
        row = self.row

        move_pattern_list = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col),
                             (row - 1, col - 1), (row + 1, col - 1), (row - 1, col + 1), (row + 1, col + 1)]

        for move in move_pattern_list:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                if opponent.has_piece_at(move[0], move[1]):
                    self._attacked_fields.add(move)
                elif current_player.has_piece_at(move[0], move[1]):
                    pass
                else:
                    self._attacked_fields.add(move)

    @override
    def update_possible_fields(self, current_player, opponent) -> None:
        self._possible_fields.clear()
        possible_fields = self._attacked_fields.copy()

        # Add Castling moves
        def is_castling_possible(rook, cols):
            # TODO implement this with a Board, so that the check for empty fields would be more efficient
            return (isinstance(rook, Rook) and
                    not rook.is_moved and
                    not self.is_moved and
                    not any(current_player.has_piece_at(self.row, col) for col in cols) and
                    not any(opponent.has_piece_at(self.row, col) for col in cols) and
                    not any((self.row, col) in opponent._attacked_fields for col in cols))

        if self._color == Color.BLACK:
            if is_castling_possible(current_player.get_piece_at(0, 0), range(1, 4)):
                possible_fields.add((0, 2))
            if is_castling_possible(current_player.get_piece_at(0, 7), range(5, 7)):
                possible_fields.add((0, 6))
        else:
            if is_castling_possible(current_player.get_piece_at(7, 0), range(1, 4)):
                possible_fields.add((7, 2))
            if is_castling_possible(current_player.get_piece_at(7, 7), range(5, 7)):
                possible_fields.add((7, 6))

        # Filter out moves that would put the king in check
        opponent.update_pieces_attacked_fields(current_player)
        opponent_attacked_fields = set()
        for piece in opponent._pieces:
            for field in piece._attacked_fields:
                opponent_attacked_fields.add(field)

        if (self.row, self.col) in opponent_attacked_fields:
            self._is_in_check = True
            # print('King is in check')
        else:
            self._is_in_check = False

        for move in possible_fields:
            if move not in opponent_attacked_fields and not self.king_in_check_after_move(move, current_player, opponent):
                self._possible_fields.add(move)

    @override
    def king_in_check_after_move(self, move, current_player, opponent) -> bool:
        result = False

        from_row = self.row
        from_col = self.col
        self.row = move[0]
        self.col = move[1]

        captured_piece = None
        if opponent.has_piece_at(move[0], move[1]):
            captured_piece = opponent.get_piece_at(move[0], move[1])
            opponent.remove_piece_at(move[0], move[1])

        opponent.update_pieces_attacked_fields(current_player)
        for piece in opponent._pieces:
            for field in piece._attacked_fields:
                if field == move:
                    result = True
                    break

        if captured_piece is not None:
            opponent.add_piece(captured_piece)

        self.row = from_row
        self.col = from_col

        for piece in opponent._pieces:
            piece.update_attacked_fields(current_player, opponent)

        return result

    @property
    def is_in_check(self) -> bool:
        return self._is_in_check


