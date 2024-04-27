from typing import Optional

from src.controller.CustomTypesForTypeHinting import ByteArray8x8, CharArray8x8
from src.model.ColorEnum import ColorEnum
import numpy as np

from src.model.Piece import Piece
from src.model.Player import Player


class Board:

    def __init__(self, white_player: Player, black_player: Player):
        self._white_player: Player = white_player
        self._black_player: Player = black_player

        self._current_player: Player = self._white_player
        self._opponent_player: Player = self._black_player

        self._selected_piece: Optional[Piece] = None

        self._piece_board = np.zeros((8, 8), dtype=np.byte)
        self._coloring_board = np.zeros((8, 8), dtype=np.character)

    def is_possible_step_at(self, x, y):
        return self._coloring_board[y][x] == 'p'

    def get_current_player(self):
        return self._current_player

    def update_board(self):
        # After initialization:

        # [[-2,-3,-4,-5,-6,-4,-3,-2],
        #  [-1,-1,-1,-1,-1,-1,-1,-1],
        #  [ 0, 0, 0, 0, 0, 0, 0, 0],
        #  [ 0, 0, 0, 0 ,0 ,0 ,0 ,0],
        #  [ 0, 0, 0, 0, 0, 0, 0, 0],
        #  [ 0, 0, 0, 0, 0, 0, 0, 0],
        #  [ 1, 1, 1, 1, 1, 1, 1, 1],
        #  [ 2, 3, 4, 5, 6, 4, 3, 2]]

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
            self._piece_board[piece.get_y()][piece.get_x()] = piece.get_type().value * piece.get_color().value

    def reset_coloring_board(self):
        self._coloring_board.fill('o')

    def update_coloring_board(self):

        self._coloring_board.fill('o')
        selected_piece = self._current_player.get_selected_piece()

        if selected_piece is not None:
            x = selected_piece.get_x()
            y = selected_piece.get_y()
            self._coloring_board[y][x] = 's'

            possible_moves = selected_piece.get_possible_moves(self)
            if possible_moves is not None:
                for move in possible_moves:
                    self._coloring_board[move[1]][move[0]] = 'p'

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

    @update_board_after
    def remove_piece_at(self, x: int, y: int) -> None:
        if not self._current_player.remove_piece_at(x, y):
            self._opponent_player.remove_piece_at(x, y)

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
        if self.is_empty_at(x, y):
            self._selected_piece = self._get_piece_at(x, y)

    def _get_piece_at(self, x: int, y: int) -> Optional[Piece]:
        if self._current_player.has_piece_at(x, y):
            return self._current_player.get_piece_at(x, y)
        elif self._opponent_player.has_piece_at(x, y):
            return self._opponent_player.get_piece_at(x, y)
        else:
            return None

    def is_empty_at(self, x: int, y: int) -> bool:
        return self._piece_board[y][x] == 0

    @property
    def color_of_selected_piece(self) -> str:
        return self._selected_piece.get_color().name

    @property
    def type_of_selected_piece(self) -> str:
        if self._selected_piece is None:
            return ''
        return self._selected_piece.get_type().name

    @property
    def selected_piece_coordinate_x(self) -> int:
        return self._selected_piece.get_x()

    @property
    def selected_piece_coordinate_y(self) -> int:
        return self._selected_piece.get_y()

    @property
    def possible_moves(self) -> list:
        return self._selected_piece.get_possible_moves(self)

    def is_selected_piece_at(self, x: int, y: int) -> bool:
        return self._coloring_board[y][x] == 'S'




