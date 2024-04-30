import functools
import time
from typing import List

from src.controller import ViewController
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.King import King
from src.model.Pawn import Pawn
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum
from src.model.Player import Player


class GameController:

    def __init__(self, white_player_name: str, black_player_name: str, view_controller: ViewController):  # type: ignore
        self._board: Board = Board()
        self._white_player: Player = Player(white_player_name, ColorEnum.WHITE, self._board)
        self._black_player: Player = Player(black_player_name, ColorEnum.BLACK, self._board)

        self._current_player: Player = self._white_player
        self._opponent_player: Player = self._black_player

        self.is_white_turn: bool = True

        self._view_controller: ViewController = view_controller
        self._board_history_prev: List[Board] = []
        self._board_history_fwd: List[Board] = []

        self.start_game()

    def start_game(self):
        self._current_player.set_opponent(self._opponent_player)
        self._opponent_player.set_opponent(self._current_player)

        self._current_player.init_pieces()
        self._opponent_player.init_pieces()

        self._current_player.update_data()
        self._opponent_player.update_data()

        self.update_view()

    def set_pieces(self, white_pieces: List[Piece], black_pieces: List[Piece]):
        self._white_player.set_pieces(white_pieces)
        self._black_player.set_pieces(black_pieces)

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

    def update_view(self) -> None:
        self._current_player.update_data()
        # Update View by sending the updated board to the view controller
        self._view_controller.update_pieces_on_board(self._board.get_piece_board())
        self._view_controller.update_board_coloring(self._board.get_coloring_board())
        self._view_controller.update_labels(str(self._white_player.get_score()), str(self._black_player.get_score()))


    def is_friend_at(self, x: int, y: int) -> bool:
        return self._current_player.has_piece_at(x, y)

    def is_opponent_at(self, x: int, y: int) -> bool:
        return self._opponent_player.has_piece_at(x, y)

    def switch_players(self) -> None:
        # multiple assignment in Python
        self._current_player, self._opponent_player = self._opponent_player, self._current_player
        self._current_player.reset_selected_piece()

    def click_on_white_button(self) -> None:
        self._view_controller.show_white_attack_board(self._board.get_white_attack_board())

    def click_on_black_button(self) -> None:
        self._view_controller.show_black_attack_board(self._board.get_black_attack_board())

    def click_on_white_protection_button(self) -> None:
        self._view_controller.show_protection_board(self._board.get_white_protection_board())

    def click_on_black_protection_button(self) -> None:
        self._view_controller.show_protection_board(self._board.get_black_protection_board())

    def click_on_board(self, x: int, y: int) -> None:

        # A selected piece is clicked -> deselect it
        if self._current_player.is_selected_piece_at(x, y):
            self._current_player.reset_selected_piece()

        # Own unselected piece is clicked -> select it
        elif self._current_player.has_piece_at(x, y):
            self._current_player.set_selected_piece(x, y)

        # Selected piece can move to the square -> move it
        elif self._current_player.is_possible_move(x, y):
            self.make_move(x, y)

        # Empty square or opponent's piece -> deselect the selected piece
        else:
            self._current_player.reset_selected_piece()

        self.update_view()

    def make_move(self, x, y):
        self._current_player.make_move(x, y)
        if self._opponent_player.has_piece_at(x, y):
            self._opponent_player.remove_piece_at(x, y)
        # self.update_data()
        self._current_player.reset_selected_piece()
        self.switch_players()

    # def update_players(self):
    #     # Normal moves
    #     self._white_player.update_normal_moves(self._board.get_piece_board())
    #     self._black_player.update_normal_moves(self._board.get_piece_board())
    #
    #     # Special moves
    #     self._current_player.reset_special_moves()
    #     if isinstance(self._current_player.selected_piece, Pawn):
    #         self._current_player.update_en_passant(self._opponent_player.get_last_moved_piece())
    #     if isinstance(self._current_player.selected_piece, King):
    #         self._current_player.update_castling(self._board)

    def save_game(self):
        # current_data = [self._board._piece_board, self._board._current_player.get_color(),
        #                 self._board._current_player_name, self._board._opponent_player_name]
        # self._board_history_prev.append()
        pass

    def load_game_prev(self):
        # self._board_history_fwd.append(self._board)
        # self._board = self._board_history_prev.pop()
        pass

    def load_game_fwd(self):
        # current_data = [self._board._current_player, self._board._opponent_player]
        # self._board_history_prev.append()
        # self._board.load_players(self._board_history_fwd.pop())
        pass

