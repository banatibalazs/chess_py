from abc import ABC, abstractmethod
from typing import Tuple, Set
from src.model.ColorEnum import ColorEnum
from src.model.PieceTypeEnum import PieceTypeEnum



class Piece(ABC):
    def __init__(self, piece_type: PieceTypeEnum, color: ColorEnum, x: int, y: int):
        self._type = piece_type
        self._color = color
        self._x = x
        self._y = y
        self._value = self._init_value()
        self._attacked_fields = set()
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

    @property
    def possible_fields(self) -> Set[Tuple[int, int]]:
        return self._possible_fields

    @property
    def protected_fields(self) -> Set[Tuple[int, int]]:
        return self._protected_fields

    @property
    def attacked_fields(self) -> Set[Tuple[int, int]]:
        return self._possible_fields

    @abstractmethod
    def update_attacked_fields(self, current_player, opponent):
        pass

    def update_protected_fields(self, current_player):
        self._protected_fields.clear()
        for field in self._attacked_fields:
            if current_player.has_piece_at(field[0], field[1]):
                self._protected_fields.add(field)
        # print("Protected fields: ", self._protected_fields)

    def update_possible_fields(self, current_player, opponent):
        self.update_protected_fields(current_player)
        # possible_fields = self._attacked_fields - self._protected_fields
        possible_fields = self._attacked_fields


        filtered = set()
        for field in possible_fields:
            if self.check_if_king_is_attacked_after_move(field, current_player, opponent):
                filtered.add(field)

        self._possible_fields = possible_fields - filtered


        # if (self.color == ColorEnum.WHITE and self.type == PieceTypeEnum.QUEEN) or \
        #         (self.type == PieceTypeEnum.KING and self.color == ColorEnum.BLACK):
        #     print(self.color.name, self.type.name, " at: ", self.coordinates, end=" ")
        #     print("Possible fields: ", possible_fields)
        #     print("Deleted fields: ", filtered)
        #     print("Filtered possible fields: ", self._possible_fields)


    def check_if_king_is_attacked_after_move(self, field, current_player, opponent) -> bool:
        result = False
        captured_piece = None
        # Save the original piece data
        from_coordinates = self.coordinates

        # # Update the attacked fields
        # current_player.update_pieces_attacked_fields(opponent)
        # opponent.update_pieces_attacked_fields(current_player)
        #
        # opponent.update_pieces_protected_fields()
        # current_player.update_pieces_protected_fields()

        # Move the piece
        self.coordinates = field
        # If opponent has a piece at the field, remove it
        if opponent.has_piece_at(field[0], field[1]):
            captured_piece = opponent.get_piece_at(field[0], field[1])
            opponent.remove_piece_at(field[0], field[1])

        # opponent.update_pieces_attacked_fields(current_player)
        # current_player.update_pieces_attacked_fields(opponent)
        #
        # opponent.update_pieces_protected_fields()
        # current_player.update_pieces_protected_fields()

        # Check if the king is attacked
        king_position = current_player._king.coordinates
        print("King position: ", king_position)

        for piece in opponent.pieces:
            piece.update_attacked_fields(current_player, opponent)
            if king_position in piece.attacked_fields:
                result = True
                break

        # Restore the original piece data
        self.coordinates = from_coordinates

        if captured_piece is not None:
            opponent.add_piece(captured_piece)


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
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def color(self):
        return self._color

    @property
    def coordinates(self):
        return self._x, self._y

    @coordinates.setter
    def coordinates(self, value):
        self._x = value[0]
        self._y = value[1]


