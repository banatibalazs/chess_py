import functools
import time
from typing import List

from src.controller import ViewController
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.King import King
from src.model.Pawn import Pawn
from src.model.PieceTypeEnum import PieceTypeEnum
from src.model.Player import Player


class GameController:

    def __init__(self, white_player_name: str, black_player_name: str, view_controller: ViewController):  # type: ignore
        self._board: Board = Board()
        self._white_player: Player = Player(white_player_name, ColorEnum.WHITE)
        self._black_player: Player = Player(black_player_name, ColorEnum.BLACK)

        self._current_player: Player = self._white_player
        self._opponent_player: Player = self._black_player

        self._view_controller: ViewController = view_controller
        self._board_history_prev: List[Board] = []
        self._board_history_fwd: List[Board] = []
        self.update_view()

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
        self.update_data()

        # Update View by sending the updated board to the view controller
        self._view_controller.update_pieces_on_board(self._board.get_piece_board())
        self._view_controller.update_board_coloring(self._board.get_coloring_board())
        self._view_controller.update_labels(str(self.white_score()), str(self.black_score()))

    @timer_decorator
    def update_data(self) -> None:
        self.update_players()
        self.update_boards()

    def update_boards(self):
        self.update_piece_board()
        self.update_coloring_board()
        self.update_attack_boards()
        self.update_protection_boards()

    def update_players(self):
        # Normal moves
        self._white_player.update_normal_moves(self._board.get_piece_board())
        self._black_player.update_normal_moves(self._board.get_piece_board())

        # Special moves
        self._current_player.reset_special_moves()
        if isinstance(self._current_player.selected_piece, Pawn):
            self._current_player.update_en_passant(self._opponent_player.get_last_moved_piece())
        if isinstance(self._current_player.selected_piece, King):
            self._current_player.update_castling(self._board)

    def update_piece_board(self) -> None:
        self._board.reset_piece_board()
        self._board.update_piece_board(self._white_player.pieces, self._black_player.pieces)

    def update_coloring_board(self):
        self._board.reset_coloring_board()
        self._board.update_coloring_board(self._current_player.selected_piece,
                                          self._current_player.possible_moves_of_selected_piece,
                                          self._current_player.special_moves)

    def update_attack_boards(self) -> None:
        self._board.reset_attack_boards()
        self._board.update_attack_boards(self._white_player.attacked_fields, self._black_player.attacked_fields)

    def update_protection_boards(self):
        self._board.reset_protection_boards()
        self._board.update_protection_boards(self._white_player.protected_fields, self._black_player.protected_fields)

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
        if self._board.is_selected_piece_at(x, y):
            self._current_player.reset_selected_piece()

        # Own unselected piece is clicked -> select it
        elif self.is_friend_at(x, y):
            self._current_player.set_selected_piece(x, y)

        # Promotion -> promote the pawn
        elif self._board.is_normal_move_at(x, y) and self.is_promotion(x, y):
            self.promote_pawn(x, y)

        # Selected piece can move to the square -> move it
        elif self._board.is_normal_move_at(x, y):
            self.normal_move(x, y)

        # En passant or castling moves -> special move
        elif self._board.is_special_move_at(x, y):
            if isinstance(self._current_player.selected_piece, King):
                self._current_player.castling(x, y)
            if isinstance(self._current_player.selected_piece, Pawn):
                self._current_player.en_passant(x, y)
            # self.update_data()
            self._current_player.reset_selected_piece()
            self.switch_players()

        # Empty square or opponent's piece -> deselect the selected piece
        elif self._board.is_empty_at(x, y) or self.is_opponent_at(x, y):
            self._current_player.reset_selected_piece()

        self.update_view()

    def promote_pawn(self, x, y):
        self._current_player.promote_pawn(x, y, PieceTypeEnum.QUEEN)
        self._current_player.reset_selected_piece()
        self.switch_players()

    def normal_move(self, x, y):
        self.set_en_passant(y)
        self._current_player.make_normal_move(x, y)
        if self._opponent_player.has_piece_at(x, y):
            self._opponent_player.remove_piece_at(x, y)
        # self.update_data()
        self._current_player.reset_selected_piece()
        self.switch_players()

    def is_promotion(self, to_x, to_y):
        return to_y == 0 or to_y == 7 and isinstance(self._current_player.selected_piece, Pawn) and \
                self._board.is_empty_at(to_x, to_y)

    def set_en_passant(self, to_y):
        # If the selected piece is a pawn and it moves two squares forward, set the en passant variable
        self._current_player.reset_en_passant()
        if isinstance(self._current_player.selected_piece, Pawn):
            if abs(self._current_player.selected_piece.y - to_y) == 2:
                print("En passant variable is set.")
                self._current_player.selected_piece.is_en_passant = True

    def reset_selected_piece(self):
        self._current_player.reset_selected_piece()

    def get_opponent_player_last_moved_piece(self):
        return self._opponent_player.get_last_moved_piece()

    def white_score(self) -> int:
        return self._white_player.get_score()

    def black_score(self) -> int:
        return self._black_player.get_score()

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

