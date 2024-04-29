import functools
import time

from src.controller.CustomTypesForTypeHinting import ByteArray8x8, CharArray8x8
from src.model.ColorEnum import ColorEnum
import numpy as np

from src.model.King import King
from src.model.Pawn import Pawn

from src.model.Player import Player


class Board:

    NORMAL_MOVE_SYMBOL = b'n'
    SPECIAL_MOVE_SYMBOL = b's'
    SELECTED_PIECE_SYMBOL = b'x'
    EMPTY_SYMBOL = b'o'

    def __init__(self, white_player: Player, black_player: Player):
        self._white_player: Player = white_player
        self._black_player: Player = black_player

        self._current_player: Player = self._white_player
        self._opponent_player: Player = self._black_player

        self._piece_board = np.zeros((8, 8), dtype=np.byte)
        self._coloring_board = np.zeros((8, 8), dtype=np.character)

        self._white_attack_board = np.zeros((8, 8), dtype=np.bool_)
        self._black_attack_board = np.zeros((8, 8), dtype=np.bool_)
        self._white_protection_board = np.zeros((8, 8), dtype=np.bool_)
        self._black_protection_board = np.zeros((8, 8), dtype=np.bool_)

    @staticmethod
    def timer_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            # print(f"Starting {func.__name__} at {start_time}")
            result = func(*args, **kwargs)
            end_time = time.time()
            # print(f"Ending {func.__name__} at {end_time}")
            print(f"{func.__name__} ran for {(end_time - start_time):.5f} seconds")
            return result

        return wrapper

    def is_normal_move_at(self, x, y):
        return self._coloring_board[y, x] == self.NORMAL_MOVE_SYMBOL

    def is_special_move_at(self, x, y):
        return self._coloring_board[y, x] == self.SPECIAL_MOVE_SYMBOL

    def is_empty_at(self, x: int, y: int) -> bool:
        return self._piece_board[y][x] == 0

    def update_data(self):
        self.update_players()
        self.update_piece_board()
        self.update_coloring_board()
        self.update_attack_boards()
        self.update_protection_boards()

    def update_piece_board(self) -> None:
        # Reset the board
        self._piece_board.fill(0)
        # Update the board with the current piece positions
        for piece in self._white_player.pieces:
            self._piece_board[piece.y][piece.x] = piece.type.value * piece.color.value

        for piece in self._black_player.pieces:
            self._piece_board[piece.y][piece.x] = piece.type.value * piece.color.value

    @timer_decorator
    def update_players(self):
        self.update_piece_board()

        self._white_player.update_normal_moves(self._piece_board)
        self._white_player.update_special_moves(self)

        self._black_player.update_normal_moves(self._piece_board)
        self._black_player.update_special_moves(self)

    def update_coloring_board(self):

        self._coloring_board.fill(self.EMPTY_SYMBOL)

        if self._current_player.selected_piece is not None:
            x = self._current_player.selected_piece.x
            y = self._current_player.selected_piece.y
            self._coloring_board[y, x] = self.SELECTED_PIECE_SYMBOL

            possible_moves = self._current_player.possible_moves_of_selected_piece
            if possible_moves is not None:
                for move in possible_moves:
                    self._coloring_board[move[1], move[0]] = self.NORMAL_MOVE_SYMBOL

    def update_special_moves(self):

        special_moves = self._current_player.special_moves
        if special_moves is not None:
            for move in special_moves:
                self._coloring_board[move[1], move[0]] = self.SPECIAL_MOVE_SYMBOL

    def update_attack_boards(self) -> None:
        self._white_attack_board.fill(False)
        self._black_attack_board.fill(False)

        attacked_by_white = self._white_player.attacked_fields
        attacked_by_black = self._black_player.attacked_fields

        for location in attacked_by_white:
            self._white_attack_board[location[0], location[1]] = True

        for location in attacked_by_black:
            self._black_attack_board[location[0], location[1]] = True

    def update_protection_boards(self):
        self._white_protection_board.fill(False)
        self._black_protection_board.fill(False)

        protected_by_white = self._white_player.protected_fields
        protected_by_black = self._black_player.protected_fields

        for location in protected_by_white:
            self._white_protection_board[location[1], location[0]] = True

        for location in protected_by_black:
            self._black_protection_board[location[1], location[0]] = True

    def square_is_attacked_by_white(self, x, y) -> bool:
        return bool(self._white_attack_board[y, x])

    def square_is_attacked_by_black(self, x, y) -> bool:
        return bool(self._black_attack_board[y, x])

    def get_coloring_board(self) -> CharArray8x8:
        return self._coloring_board

    def get_piece_board(self) -> ByteArray8x8:
        return self._piece_board

    @property
    def current_player_name(self):
        return self._current_player.get_name()

    def is_friend_at(self, x: int, y: int) -> bool:
        return self._current_player.has_piece_at(x, y)

    def is_opponent_at(self, x: int, y: int) -> bool:
        return self._opponent_player.has_piece_at(x, y)

    def switch_players(self) -> None:
        # Switch the current player and the opponent player (multiple assignment in Python)
        self._current_player, self._opponent_player = self._opponent_player, self._current_player
        self._current_player.reset_selected_piece()

    def select_piece_at(self, x: int, y: int) -> None:
        if self._current_player.has_piece_at(x, y):
            self._current_player.set_selected_piece(x, y)

    def is_selected_piece_at(self, x: int, y: int) -> bool:
        return self._coloring_board[y, x] == self.SELECTED_PIECE_SYMBOL

    def make_normal_move(self, to_x: int, to_y: int) -> None:

        self._current_player.make_normal_move(to_x, to_y)
        if self._opponent_player.has_piece_at(to_x, to_y):
            self._opponent_player.remove_piece_at(to_x, to_y)

        self.switch_players()
        self.update_data()

    def get_black_attack_board(self):
        return self._black_attack_board

    def get_white_attack_board(self):
        return self._white_attack_board


    def get_black_protection_board(self):
        return self._black_protection_board

    def get_white_protection_board(self):
        return self._white_protection_board

    def reset_selected_piece(self):
        self._current_player.reset_selected_piece()

    def make_special_move(self, x, y):
        if self._coloring_board[y, x] == self.SPECIAL_MOVE_SYMBOL:
            if isinstance(self._current_player.selected_piece, King):
                self._current_player.castling(x, y)
                self.switch_players()
            if isinstance(self._current_player.selected_piece, Pawn):
                self._current_player.en_passant(x, y)
                if self._current_player.get_color() == ColorEnum.WHITE:
                    self._opponent_player.remove_piece_at(x, y + 1)
                else:
                    self._opponent_player.remove_piece_at(x, y - 1)
                self.switch_players()

        self.update_data()

    def get_opponent_player_last_moved_piece(self):
        return self._opponent_player.get_last_moved_piece()


    def white_score(self) -> int:
        return self._white_player.get_score()

    def black_score(self) -> int:
        return self._black_player.get_score()



