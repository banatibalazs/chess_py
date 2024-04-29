from abc import ABC, abstractmethod
from typing import List, Tuple

# from src.model.Board import Board
from src.model import Board

class Piece(ABC):
    def __init__(self, piece_type, color, x, y):
        self._type = piece_type
        self._color = color
        self._x = x
        self._y = y

        self._is_moved = False
        self._is_captured = False
        self._is_castling = False
        self._is_promotion = False
        self._is_check = False
        self._is_checkmate = False
        self._is_stalemate = False

    @abstractmethod
    def get_possible_moves(self, board: Board) -> List[Tuple[int, int]]:
        pass

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


