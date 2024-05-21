from abc import ABC, abstractmethod
from typing import Tuple, Set
from src.model.enums.enums import Color
from src.model.enums.enums import PieceType


class Piece(ABC):
    def __init__(self, piece_type: PieceType, color: Color, row: int, col: int):
        self._type = piece_type
        self._color = color
        self._col = col
        self._row = row
        self._value = self._init_value()
        self._attacked_fields = set()
        self._possible_fields = set()

        self._is_moved = False

    def _init_value(self):
        if self._type == PieceType.PAWN:
            return 1
        elif self._type == PieceType.KNIGHT:
            return 3
        elif self._type == PieceType.BISHOP:
            return 3
        elif self._type == PieceType.ROOK:
            return 5
        elif self._type == PieceType.QUEEN:
            return 9
        elif self._type == PieceType.KING:
            return 100

    @property
    def possible_fields(self) -> Set[Tuple[int, int]]:
        return self._possible_fields

    @possible_fields.setter
    def possible_fields(self, value: Set[Tuple[int, int]]):
        self._possible_fields = value

    @abstractmethod
    def update_attacked_fields(self, current_player_piece_coordinates: Set[Tuple[int, int]],
                               opponent_piece_coordinates: Set[Tuple[int, int]]):
        pass

    def is_movable(self):
        return len(self._possible_fields) > 0

    def update_possible_fields(self, current_player, opponent):
        self._possible_fields.clear()
        for move in self._attacked_fields:
            if not self.king_in_check_after_move(move, current_player, opponent):
                self._possible_fields.add(move)

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

        opponent.update_pieces_attacked_fields(current_player.piece_coordinates)
        if current_player.king.coordinates in opponent._attacked_fields:
            result = True

        if captured_piece is not None:
            opponent.add_piece(captured_piece)

        # opponent.update_pieces_attacked_fields(current_player.piece_coordinates)
        self.row = from_row
        self.col = from_col

        return result

    @property
    def value(self) -> int:
        return self._value

    @property
    def is_moved(self):
        return self._is_moved

    @is_moved.setter
    def is_moved(self, value: bool):
        self._is_moved = value

    @property
    def type(self):
        return self._type

    @property
    def col(self) -> int:
        return self._col

    @col.setter
    def col(self, value: int):
        self._col = value

    @property
    def row(self) -> int:
        return self._row

    @row.setter
    def row(self, value: int):
        self._row = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: Color):
        self._color = value

    @property
    def coordinates(self):
        return self._row, self._col

    @coordinates.setter
    def coordinates(self, value):
        self.row, self.col = value
