from src.model.Board import Board
from src.model.PieceType import PieceType


class GameController:

    SELECTED_COLOR = "red"


    def __init__(self, white_player_name, black_player_name, view_controller):
        self._board = Board(white_player_name, black_player_name)
        self._is_white_turn = True
        self._selected_piece = None
        self._view_controller = view_controller
        self._boardHistory = []
        self.update_view()

    def update_view(self):
        self._view_controller.update_board(self._board.get_int_board())

    def click_on_square(self, x, y):

        value = self._board.get_value_at(x, y)

        if value == 0:
            print("Empty square selected")

        elif value < 0 and not self._is_white_turn:
            print("Black piece selected")
            self.select_piece(x, y)

        elif value > 0 and self._is_white_turn:
            print("White piece selected")
            self.select_piece(x, y)


    def select_piece(self, x, y):
        print("Piece selected at ", x, y)

        self.color_selected_square(x, y)


    def color_selected_square(self, x, y):
        self._view_controller.update_square_color(GameController.SELECTED_COLOR, x, y)

    def step(self):
        pass

    def save_game(self):
        pass

    def load_game(self):
        pass