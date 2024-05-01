from abc import ABC, abstractmethod
from typing import List, Tuple, Set

from src.controller.CustomTypesForTypeHinting import ByteArray8x8
import src.model.Board as Board
from src.model.PieceTypeEnum import PieceTypeEnum


class Piece(ABC):
    def __init__(self, piece_type, color, x, y):
        self._type = piece_type
        self._color = color
        self._x = x
        self._y = y
        self._value = self._init_value()
        self._possible_fields = set()
        self._protected_fields = set()

        self._is_moved = False
        self._is_captured = False
        self._is_castling = False
        self._is_promotion = False
        self._is_check = False
        self._is_checkmate = False
        self._is_stalemate = False

    def _init_value(self):
        if self._type == PieceTypeEnum.PAWN:
            return 1
        elif self._type == PieceTypeEnum.KNIGHT:
            return 3
        elif self._type == PieceTypeEnum.BISHOP:
            return 3
        elif self._type == PieceTypeEnum.ROOK:
            return 5
        elif self._type == PieceTypeEnum.QUEEN:
            return 9
        elif self._type == PieceTypeEnum.KING:
            return 100

    def get_possible_fields(self) -> Set[Tuple[int, int]]:
        return self._possible_fields

    def get_protected_fields(self) -> Set[Tuple[int, int]]:
        return self._protected_fields

    @abstractmethod
    def update_piece(self, board: Board):
        pass

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
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def color(self):
        return self._color

    def set_coordinates(self, x, y):
        self._x = x
        self._y = y

    @property
    def coordinates(self):
        return self._x, self._y


