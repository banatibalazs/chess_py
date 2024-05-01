import functools
import time
from typing import List

from src.controller import ViewController
from src.controller.TimerThread import TimerThread
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.Player import Player


class GameController:

    def __init__(self, white_player_name: str, black_player_name: str, view_controller: ViewController):  # type: ignore
        self._board: Board = Board()
        self._white_player: Player = Player(white_player_name, ColorEnum.WHITE, self._board)
        self._black_player: Player = Player(black_player_name, ColorEnum.BLACK, self._board)

        self.white_timer = TimerThread(300, white_player_name, self)  # 5 minutes timer
        self.black_timer = TimerThread(300, black_player_name, self)  # 5 minutes timer

        self._current_player: Player = self._white_player
        self._opponent_player: Player = self._black_player

        self.is_white_turn: bool = True

        self._view_controller: ViewController = view_controller
        self._board_history_prev: List[Board] = []
        self._board_history_fwd: List[Board] = []

        self.start_game()

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

    def start_game(self):
        self._white_player.init_pieces()
        self._black_player.init_pieces()

        self.update_boards()
        self.update_players()
        self.update_view()


    def next_turn(self):
        self.update_boards()
        self.update_players()
        self.update_view()
        self.is_white_turn = not self.is_white_turn
        self.switch_players()

        if not self.is_white_turn:
            print("--------------------------------------------------------------------------------")
            print(" Black player's turn")
            # self._current_player.choose_movable_piece()
            # print("Selected piece: ", self._current_player.selected_piece)
            # print("At position: ", self._current_player.selected_piece.x, self._current_player.selected_piece.y)
            # print("Type: ", self._current_player.selected_piece.type)
            # print("Color: ", self._current_player.selected_piece.color)
            # move = self._black_player.choose_step()
            # print("Move: ", move)
            # print("--------------------------------------------------------------------------------")



    # @timer_decorator
    def update_players(self):

        self._white_player.update_pieces_data()
        self._black_player.update_pieces_data()
        # 1. Update possible moves of selected piece
        self._white_player.get_possible_moves_of_selected_piece()
        self._black_player.get_possible_moves_of_selected_piece()

        # 2. Update special moves (castling, en passant) - later maybe promotion
        self._white_player.get_special_moves(self._opponent_player.last_moved_piece)
        self._black_player.get_special_moves(self._opponent_player.last_moved_piece)

        # 3-4. Update attacked locations
        #      Update protected fields
        self._white_player.update_protected_and_attacked_fields()
        self._black_player.update_protected_and_attacked_fields()



    # @timer_decorator
    def update_boards(self) -> None:
        # It has the following boards:
        # 1. Piece board -> the positions of the pieces
        # 2. Coloring board -> the coloring of the squares (view)
        # 3. Attack boards -> the attacked fields by the players
        # 4. Protection boards -> the protected fields by the players

        if self._current_player._color == ColorEnum.WHITE:
            # The boards methods' parameters are the white player's data first, then the black player's data
            self._board.update_piece_board(self._current_player.pieces, self._opponent_player.pieces)
            self._board.update_attack_boards(self._current_player.attacked_fields, self._opponent_player.attacked_fields)
            self._board.update_protection_boards(self._current_player.protected_fields, self._opponent_player.protected_fields)
        else:
            self._board.update_piece_board(self._opponent_player.pieces, self._current_player.pieces)
            self._board.update_attack_boards(self._opponent_player.attacked_fields, self._current_player.attacked_fields)
            self._board.update_protection_boards(self._opponent_player.protected_fields, self._current_player.protected_fields)

        self._board.update_coloring_board(self._current_player.selected_piece, self._current_player.special_moves)

    def update_view(self) -> None:
        self.update_players()
        self.update_boards()
        # self._current_player.update_data(self._opponent_player)
        # Update View by sending the updated board to the view controller
        self._view_controller.update_pieces_on_board(self._board.get_piece_board())
        self._view_controller.update_board_coloring(self._board.get_coloring_board())
        self._view_controller.update_labels(str(self._white_player.get_score()), str(self._black_player.get_score()))

    def switch_players(self) -> None:
        # multiple assignment in Python
        self._current_player, self._opponent_player = self._opponent_player, self._current_player
        self._current_player.reset_selected_piece()

    def click_on_white_button(self) -> None:
        self._view_controller.show_white_attack_board(self._board.get_white_attack_board())

    def print_piece_board(self):
        piece_board = self._board.get_piece_board()
        for row in piece_board:
            print(row)

    def print_coloring_board(self):
        coloring_board = self._board.get_coloring_board()
        for row in coloring_board:
            print(row)

    def print_attack_board(self):
        white_attack_board = self._board.get_white_attack_board()
        black_attack_board = self._board.get_black_attack_board()
        print("White attack board:")
        for row in white_attack_board:
            print(row)

        print("--------------------------------------------------------------------------------\n")

        print("Black attack board:")
        for row in black_attack_board:
            print(row)

    def click_on_black_button(self) -> None:
        self._view_controller.show_black_attack_board(self._board.get_black_attack_board())
        # print("--------------------------------------------------------------------------------\n")
        # print("Piece board:")
        # self.print_piece_board()
        # print("--------------------------------------------------------------------------------\n")
        # print("Coloring board:")
        # self.print_coloring_board()
        # print("--------------------------------------------------------------------------------\n")
        # print("Attack board:")
        # self.print_attack_board()
        # print("--------------------------------------------------------------------------------\n")

    def click_on_white_protection_button(self) -> None:
        self._view_controller.show_protection_board(self._board.get_white_protection_board())

    def click_on_black_protection_button(self) -> None:
        self._view_controller.show_protection_board(self._board.get_black_protection_board())

    def click_on_board(self, x: int, y: int) -> None:

        # A selected piece is clicked -> deselect it
        if self._current_player.is_selected_piece_at(x, y):
            print("Deselecting piece")
            self._current_player.reset_selected_piece()

        # Own unselected piece is clicked -> select it
        elif self._current_player.has_piece_at(x, y):
            print("Selecting piece")
            self._current_player.set_selected_piece(x, y)

        # Selected piece can move to the square -> move it
        elif self._current_player.is_possible_move(x, y):
            print("Making move")
            self.make_move(x, y)

        # Empty square or opponent's piece -> deselect the selected piece
        else:
            print("Empty.")
            self._current_player.reset_selected_piece()

        self.update_view()

    def make_move(self, x, y):
        self._current_player.make_move(x, y, self._opponent_player)
        if self._opponent_player.has_piece_at(x, y):
            self._opponent_player.remove_piece_at(x, y)
        # self.update_data()
        self._current_player.reset_selected_piece()
        self.next_turn()

    def save_game(self):
        # current_data = [self._board._piece_board, self._board._current_player.get_color(),
        #                 self._board._current_player_name, self._board._opponent_player_name]
        # self._board_history_prev.append()
        pass

    def set_pieces(self, white_pieces: List[Piece], black_pieces: List[Piece]):
        self._white_player.set_pieces(white_pieces)
        self._black_player.set_pieces(black_pieces)

    def load_game_prev(self):
        # self._board_history_fwd.append(self._board)
        # self._board = self._board_history_prev.pop()
        pass

    def load_game_fwd(self):
        # current_data = [self._board._current_player, self._board._opponent_player]
        # self._board_history_prev.append()
        # self._board.load_players(self._board_history_fwd.pop())
        pass

