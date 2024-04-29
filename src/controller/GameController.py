import functools
import time
from typing import List

from src.controller import ViewController
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.King import King
from src.model.Pawn import Pawn
from src.model.Player import Player


class GameController:

    NORMAL_MOVE_SYMBOL = b'n'
    SPECIAL_MOVE_SYMBOL = b's'
    SELECTED_PIECE_SYMBOL = b'x'
    EMPTY_SYMBOL = b'o'

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

    def update_data(self) -> None:
        self.update_players()
        self.update_piece_board()
        self.update_coloring_board()
        self.update_attack_boards()
        self.update_protection_boards()

    def update_piece_board(self) -> None:
        # Reset the board
        self._board._piece_board.fill(0)
        # Update the board with the current piece positions
        for piece in self._white_player.pieces:
            self._board._piece_board[piece.y][piece.x] = piece.type.value * piece.color.value

        for piece in self._black_player.pieces:
            self._board._piece_board[piece.y][piece.x] = piece.type.value * piece.color.value


    def update_coloring_board(self):

        self._board._coloring_board.fill(self.EMPTY_SYMBOL)

        if self._current_player.selected_piece is not None:
            x = self._current_player.selected_piece.x
            y = self._current_player.selected_piece.y
            self._board._coloring_board[y, x] = self.SELECTED_PIECE_SYMBOL

            possible_moves = self._current_player.possible_moves_of_selected_piece
            if possible_moves is not None:
                for move in possible_moves:
                    self._board._coloring_board[move[1], move[0]] = self.NORMAL_MOVE_SYMBOL

            self.update_special_moves()


    def update_special_moves(self):

        special_moves = self._current_player.special_moves
        if special_moves is not None:
            for move in special_moves:
                self._board._coloring_board[move[1], move[0]] = self.SPECIAL_MOVE_SYMBOL

    def update_attack_boards(self) -> None:
        self._board._white_attack_board.fill(False)
        self._board._black_attack_board.fill(False)

        attacked_by_white = self._white_player.attacked_fields
        attacked_by_black = self._black_player.attacked_fields

        for location in attacked_by_white:
            self._board._white_attack_board[location[0], location[1]] = True

        for location in attacked_by_black:
            self._board._black_attack_board[location[0], location[1]] = True

    def update_protection_boards(self):
        self._board._white_protection_board.fill(False)
        self._board._black_protection_board.fill(False)

        protected_by_white = self._white_player.protected_fields
        protected_by_black = self._black_player.protected_fields

        for location in protected_by_white:
            self._board._white_protection_board[location[1], location[0]] = True

        for location in protected_by_black:
            self._board._black_protection_board[location[1], location[0]] = True

    def update_players(self):
        self._white_player.update_normal_moves(self._board.get_piece_board())
        self._white_player.update_special_moves(self._board, self._black_player.get_last_moved_piece())

        self._black_player.update_normal_moves(self._board.get_piece_board())
        self._black_player.update_special_moves(self._board, self._white_player.get_last_moved_piece())

    def is_friend_at(self, x: int, y: int) -> bool:
        return self._current_player.has_piece_at(x, y)

    def is_opponent_at(self, x: int, y: int) -> bool:
        return self._opponent_player.has_piece_at(x, y)

    def update_view(self) -> None:

        # Update the board state
        self.update_data()
        # Update View by sending the updated board to the view controller
        self._view_controller.update_pieces_on_board(self._board.get_piece_board())
        self._view_controller.update_board_coloring(self._board.get_coloring_board())
        # Update View labels
        self._view_controller.update_labels(str(self.white_score()),
                                            str(self.black_score()))

    def click_on_board(self, x: int, y: int) -> None:

        # If square is selected then deselect it
        if self._board.is_selected_piece_at(x, y):
            self._current_player.reset_selected_piece()

        # If square contains a piece owned by the current player then select piece
        elif self.is_friend_at(x, y):
            self._current_player.set_selected_piece(x, y)

        # If square is in the possible moves of the selected piece then move the selected piece to (x,y)
        elif self._board.is_normal_move_at(x, y):
            self.make_normal_move(x, y)

        elif self._board.is_special_move_at(x, y):
            self.make_special_move(x,y)

        # Check if the square is empty
        elif self._board.is_empty_at(x, y) or self.is_opponent_at(x, y):
            self.reset_selected_piece()

        self.update_view()


    def make_normal_move(self, to_x: int, to_y: int) -> None:

        self._current_player.make_normal_move(to_x, to_y)
        if self._opponent_player.has_piece_at(to_x, to_y):
            self._opponent_player.remove_piece_at(to_x, to_y)

        self.switch_players()
        self.update_data()

    def make_move(self, x: int, y: int) -> None:



        self.switch_players()

    def switch_players(self) -> None:
        # Switch the current player and the opponent player (multiple assignment in Python)
        self._current_player, self._opponent_player = self._opponent_player, self._current_player
        self._current_player.reset_selected_piece()

    def make_special_move(self, x, y):
        if self._board._coloring_board[y, x] == self.SPECIAL_MOVE_SYMBOL:
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

    def click_on_white_button(self) -> None:
        self._view_controller.show_white_attack_board(self._board.get_white_attack_board())

    def click_on_black_button(self) -> None:
        self._view_controller.show_black_attack_board(self._board.get_black_attack_board())

    def click_on_white_protection_button(self) -> None:
        self._view_controller.show_protection_board(self._board.get_white_protection_board())

    def click_on_black_protection_button(self) -> None:
        self._view_controller.show_protection_board(self._board.get_black_protection_board())

