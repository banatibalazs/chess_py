from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.Player import Player


class GameController:
    SELECTED_COLOR = "red"

    def __init__(self, white_player_name, black_player_name, view_controller):
        self._white_player = Player(white_player_name, ColorEnum.WHITE)
        self._black_player = Player(black_player_name, ColorEnum.BLACK)
        self._current_player = self._white_player

        self._board = Board(self._white_player.get_pieces(), self._black_player.get_pieces())

        self._view_controller = view_controller
        self._boardHistory = []
        self.update_view()

    def update_view(self):

        self._board.update_board(self._white_player.get_pieces(), self._black_player.get_pieces())
        self._board.update_coloring_board(self._current_player.get_selected_piece())

        self._view_controller.update_board_view(self._board.get_piece_board(),
                                                self._board.get_coloring_board(),
                                                self._board.get_possible_squares())

    def handle_click(self, x, y):
        pass
        #if clicked piece is selected, deselect it

        #if clicked square contains a selected piece, deselect it

        #if clicked square is a possible move, move the piece

    def click_on_square(self, x, y):

        color = self._board.get_color_at(x, y)

        if color == ColorEnum.NONE:
            print("Empty square clicked.")

        elif color != self._current_player.get_color():
            print(f"Clicked on a {color} piece. Your color is {self._current_player.get_color()}.")

        elif color == self._current_player.get_color():
            print(f"{color} piece selected by {self._white_player.get_name()}.")
            self.handle_selection(x, y)

    def handle_selection(self, x, y):
        self._current_player.select_piece(x, y)
        self.update_view()

    def step(self):
        pass

    def save_game(self):
        pass

    def load_game(self):
        pass
