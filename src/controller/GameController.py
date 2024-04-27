from typing import List
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
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

        # Update the pieces
        self._view_controller.update_pieces_on_board(self._board.get_piece_board())

        # Update the coloring
        self._view_controller.update_board_coloring(self._board.get_coloring_board())

        # self.print_boards()

    def print_boards(self) -> None:
        print("\tPiece Board:\t\t\tColoring Board:")
        for i in range(8):
            print(str(self._board.get_piece_board()[i]).replace('[', ' ')
                  .replace(' ', '  ')
                  .replace(" -", "-")
                  .replace("]", "")
                  .ljust(30) + "   " +
                  str(self._board.get_coloring_board()[i]).ljust(30))

    def click_on_board(self, x: int, y: int) -> None:

        # Check if the square is empty
        if self._board.is_empty_at(x, y) or self._board.is_opponent_at(x, y):
            print("No piece selected.")

        # If square contains a selected piece then deselect it
        elif self._board.is_selected_piece_at(x, y):
            self._board.reset_selected_piece()
            print("Piece deselected by {self._board.current_player_name}.")

        # If square contains piece owned by the current player then select piece
        elif self._board.is_friend_at(x, y):
            self._board.select_piece_at(x, y)
            print(f"Piece selected by {self._board.current_player_name}.")
            print(f"Piece selected at"
                  f" x: {self._board.selected_piece_coordinate_x}"
                  f" y: {self._board.selected_piece_coordinate_y}")

        # If square is in the possible moves of the selected piece then move the selected piece to (x,y)
        elif self._board.is_possible_step_at(x, y):
            self.step(x, y)

        self.update_view()

    def step(self, x: int, y: int) -> None:

        print(f"Step made by {self._board.current_player_name}.")

        # Save the current board state
        # self._boardHistory.append(copy.deepcopy(self._current_player), self._opponent_player)

        moving_piece = self._board.selected_piece
        moving_piece.set_coordinates(x, y)
        moving_piece.set_moved()

        # Check if promotion
        # if moving_piece.get_type() ==  and (y == 0 or y == 7):
        #     self._current_player.promote_pawn(moving_piece, 'QUEEN')
        #     print(f"{self._current_player.get_name()} promoted a pawn to a queen.")

        # Check if capture
        if self._board.is_opponent_at(x, y):
            print(f"Capture made by {self._board.current_player_name}.")
            self._board.remove_piece_at(x, y)
            print(f"{self._board.opponent_player_name} lost a piece.")
            print(f"{self._board.opponent_player_name} has {self._board.opponent_player_piece_number} pieces.")
            print(f"{self._board.current_player_name} has {self._board.current_player_piece_number} pieces.")

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
