from typing import Optional

from src.controller.CustomTypesForTypeHinting import ByteArray8x8, CharArray8x8
from src.model.ColorEnum import ColorEnum
import numpy as np

from src.model.Piece import Piece
from src.model.Player import Player


class Board:

    POSSIBLE_MOVE_SYMBOL = b'p'
    SELECTED_PIECE_SYMBOL = b's'
    EMPTY_SYMBOL = b'o'

    def __init__(self, white_player: Player, black_player: Player):
        self._white_player: Player = white_player
        self._black_player: Player = black_player

        self._current_player: Player = self._white_player
        self._opponent_player: Player = self._black_player

        self._selected_piece: Optional[Piece] = None

        self._piece_board = np.zeros((8, 8), dtype=np.byte)
        self._coloring_board = np.zeros((8, 8), dtype=np.character)

        self._white_attack_board = np.zeros((8, 8), dtype=np.bool_)
        self._black_attack_board = np.zeros((8, 8), dtype=np.bool_)

    def is_possible_step_at(self, x, y):
        return self._coloring_board[y, x] == self.POSSIBLE_MOVE_SYMBOL

    def get_current_player(self):
        return self._current_player

    def update_board(self):
        # Reset the board to all 0s
        self._piece_board.fill(0)
        # Update the board with the current piece positions
        self.update_piece_positions(self._white_player.get_pieces())
        self.update_piece_positions(self._black_player.get_pieces())
        # Update the coloring board
        self.update_coloring_board()

    @staticmethod
    def update_board_after(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.update_board()
            return result

        return wrapper

    def update_piece_positions(self, pieces):
        for piece in pieces:
            self._piece_board[piece.y][piece.x] = piece.type.value * piece.color.value

    def reset_coloring_board(self):
        self._coloring_board.fill(self.EMPTY_SYMBOL)

    def update_coloring_board(self):

        self._coloring_board.fill(self.EMPTY_SYMBOL)

        if self._selected_piece is not None:
            x = self._selected_piece.x
            y = self._selected_piece.y
            self._coloring_board[y, x] = self.SELECTED_PIECE_SYMBOL

            possible_moves = self._selected_piece.get_possible_moves(self)
            if possible_moves is not None:
                for move in possible_moves:
                    self._coloring_board[move[1], move[0]] = self.POSSIBLE_MOVE_SYMBOL

    def get_value_at(self, x, y):
        # Get the value of the piece at the given coordinates
        return self._piece_board[y][x]

    def get_color_at(self, x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return ColorEnum.NONE
        # Get the color of the piece at the given coordinates
        if self._piece_board[y][x] < 0:
            return ColorEnum.BLACK
        elif self._piece_board[y][x] > 0:
            return ColorEnum.WHITE
        else:
            return ColorEnum.NONE

    def is_empty(self, x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        return self.get_value_at(x, y) == 0

    def is_enemy(self, x, y, color):
        return self.get_color_at(x, y) != color and self.get_color_at(x, y) != ColorEnum.NONE

    def get_coloring_board(self) -> CharArray8x8:
        return self._coloring_board

    def get_piece_board(self) -> ByteArray8x8:
        return self._piece_board

    @property
    def current_player_name(self):
        return self._current_player.get_name()

    @property
    def opponent_player_name(self):
        return self._opponent_player.get_name()

    @property
    def opponent_player_piece_number(self) -> int:
        return self._opponent_player.get_piece_number()

    @property
    def current_player_piece_number(self) -> int:
        return self._current_player.get_piece_number()

    @property
    def current_player_color(self) -> ColorEnum:
        return self._current_player.get_color()

    @property
    def opponent_player_color(self) -> ColorEnum:
        return self._opponent_player.get_color()

    def is_friend_at(self, x: int, y: int) -> bool:
        return self._current_player.has_piece_at(x, y)

    def is_opponent_at(self, x: int, y: int) -> bool:
        return self._opponent_player.has_piece_at(x, y)

    def switch_players(self) -> None:
        # Switch the current player and the opponent player (multiple assignment in Python)
        self._current_player, self._opponent_player = self._opponent_player, self._current_player
        self.reset_selected_piece()

    @property
    def selected_piece(self) -> Optional[Piece]:
        return self._selected_piece

    @update_board_after
    def reset_selected_piece(self) -> None:
        self._selected_piece = None

    def has_selected_piece(self) -> bool:
        return self._selected_piece is not None

    @update_board_after
    def move_piece(self, piece: Piece, x: int, y: int):
        pass

    @update_board_after
    def remove_piece(self, piece: Piece) -> None:
        pass

    @update_board_after
    def select_piece_at(self, x: int, y: int) -> None:
        if self._current_player.has_piece_at(x, y):
            self._selected_piece = self._current_player.get_piece_at(x, y)

    def is_empty_at(self, x: int, y: int) -> bool:
        return self._piece_board[y][x] == 0

    @property
    def color_of_selected_piece(self) -> str:
        return self._selected_piece.color.name

    @property
    def type_of_selected_piece(self) -> str:
        if self._selected_piece is None:
            return ''
        return self._selected_piece.type.name

    @property
    def selected_piece_coordinate_x(self) -> int:
        return self._selected_piece.x

    @property
    def selected_piece_coordinate_y(self) -> int:
        return self._selected_piece.y

    @property
    def possible_moves(self) -> list:
        return self._selected_piece.get_possible_moves(self)

    def is_selected_piece_at(self, x: int, y: int) -> bool:
        return self._coloring_board[y][x] == self.SELECTED_PIECE_SYMBOL

    def move_piece_to(self, to_x: int, to_y: int) -> None:
        # if self._selected_piece.get_type() == 'PAWN' and (to_y == 0 or to_y == 7):
        from_x, from_y = self._selected_piece.coordinates

        self._selected_piece.set_coordinates(to_x, to_y)
        self.capture_piece_at(to_x, to_y)
        self._selected_piece.set_moved()

        self.switch_players()

    def check_en_passant(self, x: int, y: int) -> bool:
        pass

    @update_board_after
    def capture_piece_at(self, x: int, y: int) -> None:
        if self._opponent_player.has_piece_at(x, y):
            self._opponent_player.remove_piece_at(x, y)





