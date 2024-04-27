from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, piece_type, color, x, y):
        self._type = piece_type
        self._color = color
        self._x = x
        self._y = y

        self._is_moved = False
        self._is_captured = False
        self._is_en_passant = False
        self._is_castling = False
        self._is_promotion = False
        self._is_check = False
        self._is_checkmate = False
        self._is_stalemate = False

    @abstractmethod
    def get_possible_moves(self, board):
        pass

    def set_moved(self):
        self._is_moved = True

    def is_moved(self):
        return self._is_moved

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

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    def set_coordinates(self, x, y):
        self._x = x
        self._y = y

    @property
    def coordinates(self):
        return self._x, self._y


