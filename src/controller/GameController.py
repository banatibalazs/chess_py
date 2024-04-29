from typing import List

from src.controller import ViewController
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.Player import Player


class GameController:

    def __init__(self, white_player_name: str, black_player_name: str, view_controller: ViewController):  # type: ignore
        self._board: Board = Board(Player(white_player_name, ColorEnum.WHITE),
                                   Player(black_player_name, ColorEnum.BLACK))

        self._view_controller: ViewController = view_controller
        self._boardHistory: List[Board] = []
        self.update_view()

    def update_view(self) -> None:

        # Update the board state
        self._board.update_data()
        # Update View by sending the updated board to the view controller
        self._view_controller.update_pieces_on_board(self._board.get_piece_board())
        self._view_controller.update_board_coloring(self._board.get_coloring_board())
        # Update View labels
        self._view_controller.update_labels(str(self._board.white_score()),
                                            str(self._board.black_score()))

    def click_on_board(self, x: int, y: int) -> None:

        # If square is selected then deselect it
        if self._board.is_selected_piece_at(x, y):
            self._board.reset_selected_piece()

        # If square contains a piece owned by the current player then select piece
        elif self._board.is_friend_at(x, y):
            self._board.select_piece_at(x, y)

        # If square is in the possible moves of the selected piece then move the selected piece to (x,y)
        elif self._board.is_normal_move_at(x, y):
            self._board.make_normal_move(x, y)

        elif self._board.is_special_move_at(x, y):
            self._board.make_special_move(x,y)

        # Check if the square is empty
        elif self._board.is_empty_at(x, y) or self._board.is_opponent_at(x, y):
            self._board.reset_selected_piece()

        self.update_view()

    def save_game(self):
        pass

    def load_game(self):
        pass

    def click_on_white_button(self) -> None:
        self._view_controller.show_white_attack_board(self._board.get_white_attack_board())

    def click_on_black_button(self) -> None:
        self._view_controller.show_black_attack_board(self._board.get_black_attack_board())

    def click_on_white_protection_button(self) -> None:
        self._view_controller.show_protection_board(self._board.get_white_protection_board())

    def click_on_black_protection_button(self) -> None:
        self._view_controller.show_protection_board(self._board.get_black_protection_board())

