import copy

import numpy as np

import src.model.Board as Board

from abc import ABC, abstractmethod
from typing import Tuple, Set, List

from src.controller.CustomTypesForTypeHinting import ByteArray8x8
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


    def update_possible_fields(self, current_player, opponent):
        possible_fields = self._attacked_fields - self._protected_fields
        filtered = set()
        # print("Possible fields: ", possible_fields)
        for field in possible_fields:
            if self.check_if_king_is_attacked_after_move(field, current_player, opponent):
                filtered.add(field)
        # print("Filtered: ", filtered)
        self._possible_fields = possible_fields - filtered


    def check_if_king_is_attacked_after_move(self, field, current_player, opponent) -> bool:
        result = False
        to_x, to_y = field

        # Update the piece board
        # current_player._board.update_piece_board(current_player.pieces, opponent.pieces)

        # Update the attacked fields
        # current_player.update_pieces_attacked_fields()
        # opponent.update_pieces_attacked_fields()

        # Change the piece position
        # self.set_coordinates(to_x, to_y)
        # if opponent.has_piece_at(to_x, to_y):






        # # Copy the board
        # copy_piece_board = copy.deepcopy(current_player._board.get_piece_board())
        #
        # # Get the king position
        # if self.color == ColorEnum.WHITE:
        #     own_king_y, own_king_x = np.where(copy_piece_board == 6)
        # else:
        #     own_king_y, own_king_x = np.where(copy_piece_board == -6)
        #
        # own_king_y = int(own_king_y[0])
        # own_king_x = int(own_king_x[0])
        #
        # # Moving piece data
        # from_x, from_y = self.x, self.y
        # to_x, to_y = move
        # value = self._type.value
        # color = self.color
        #
        # # Move the piece
        # copy_piece_board[from_y, from_x] = 0
        # copy_piece_board[to_y, to_x] = value if color == ColorEnum.WHITE else -value
        #
        #
        # # Update update opponents attack fields
        # for piece in opponent_pieces:
        #     piece.update_attacked_fields(copy_piece_board)
        #
        # # Check if the king is attacked
        # for piece in opponent_pieces:
        #     # If capture happened, omit the captured piece
        #     if piece.x == to_x and piece.y == to_y:
        #         continue
        #     if (own_king_x, own_king_y) in piece._attacked_fields:
        #         result = True
        #         print("Own king: ", (own_king_x, own_king_y), "Attacked fields: ", piece._attacked_fields, end=' ')
        #         print((own_king_x, own_king_y) in piece._attacked_fields)
        #         # print("King is attacked after move")
        #         break
        #
        # # Restore the original piece data
        # for piece in opponent_pieces:
        #     piece.update_attacked_fields(original_piece_board)

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

    def set_coordinates(self, x, y):
        self._x = x
        self._y = y

    @property
    def coordinates(self):
        return self._x, self._y


