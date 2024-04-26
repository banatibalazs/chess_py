from typing import List
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.Player import Player
import src.controller.ViewController as ViewController


class GameController:

    def __init__(self, white_player_name: str, black_player_name: str, view_controller: ViewController):
        self._board: Board = Board(Player(white_player_name, ColorEnum.WHITE),
                                   Player(black_player_name, ColorEnum.BLACK))

        self._view_controller: ViewController = view_controller
        self._boardHistory: List[Board] = []
        self.update_view()

    def update_view(self) -> None:

        # Update the board
        self._board.update_board()

        # Check if a piece is selected
        if self._board.has_selected_piece():
            self._board.update_coloring_board()
        else:
            # If no piece is selected, reset the coloring board
            self._board.reset_coloring_board()
            print("No piece selected.")

        # Send the updated board to the view controller
        self._view_controller.update_board_view(self._board.get_piece_board(),
                                                self._board.get_coloring_board())

    def click_on_square(self, x: int, y: int) -> None:

        if self._board.is_possible_step_at(x, y):
            self.step(x, y)
        else:
            if self._board.current_player_has_piece_at(x, y):
                self._board.set_selected_piece(x, y)
                print(f"{piece.get_color().name} {piece.get_type().name} piece at position:"
                      f" x: {piece.get_x()} y: {piece.get_y()} selected by {self._board.get_current_player_name()}.")
                self.handle_selection(x, y)
            else:
                print("No piece selected.")

    def handle_selection(self, x: int, y: int) -> None:
        if self._current_player.has_selected_piece() and self._current_player.get_selected_piece().get_coordinates() == (
        x, y):
            print("Deselected piece.")
            self._current_player.reset_selected_piece()

        elif self._current_player.has_piece_at(x, y):
            print("Selected piece.")
            self._current_player.set_selected_piece(x, y)
            self.get_possible_moves(x, y, self._current_player.get_selected_piece())

        self.update_view()

    def get_possible_moves(self, x: int, y: int, piece: Piece) -> None:
        self._board.update_coloring_board()

    def step(self, x: int, y: int) -> None:

        print(f"Step made by {self._board.get_current_player_name()}.")

        # Save the current board state
        # self._boardHistory.append(copy.deepcopy(self._current_player), self._opponent_player)

        moving_piece = self._board.get_selected_piece()
        moving_piece.set_coordinates(x, y)
        moving_piece.set_moved()

        # Check if promotion
        # if moving_piece.get_type() ==  and (y == 0 or y == 7):
        #     self._current_player.promote_pawn(moving_piece, 'QUEEN')
        #     print(f"{self._current_player.get_name()} promoted a pawn to a queen.")

        # Check if capture
        if self._board.opponent_has_piece_at(x, y):
            print(f"Capture made by {self._board.get_current_player_name()}.")
            self._board.remove_piece_at(x, y)
            print(f"{self._board.get_opponent_player_name()} lost a piece.")
            print(f"{self._board.get_opponent_player_name()} has {self._board.get_opponent_player_piece_number()} pieces.")
            print(f"{self._board.get_current_player_name()} has {self._board.get_current_player_piece_number()} pieces.")

        # Check if castling

        # Check if en passant

        # Check if check

        # Check if checkmate

        # print(f"{self._opponent_player.get_name()} is in check.")
        # if piece.is_checkmate(self._board):
        #     print(f"{self._opponent_player.get_name()} is in checkmate.")
        #     print(f"{self._current_player.get_name()} won the game.")
        #     return

        # Check if stalemate

        # Switch player
        self._board.switch_players()

        self.update_view()

    def save_game(self):
        pass

    def load_game(self):
        pass
