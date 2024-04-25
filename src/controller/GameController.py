from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.Player import Player


class GameController:
    SELECTED_COLOR = "red"

    def __init__(self, white_player_name, black_player_name, view_controller):
        self._white_player = Player(white_player_name, ColorEnum.WHITE)
        self._black_player = Player(black_player_name, ColorEnum.BLACK)
        self._current_player = self._white_player
        self._opponent_player = self._black_player

        self._board = Board(self._white_player.get_pieces(), self._black_player.get_pieces())

        self._view_controller = view_controller
        self._boardHistory = []
        self.update_view()

    def update_view(self):

        self._board.update_board(self._white_player.get_pieces(), self._black_player.get_pieces())

        if self._current_player.has_selected_piece():
            self._board.update_coloring_board(self._current_player.get_selected_piece(),
                                              self._current_player.get_selected_piece().get_possible_moves(self._board))
        else:
            self._board.reset_coloring_board()
            print("No piece selected.")

        self._view_controller.update_board_view(self._board.get_piece_board(),
                                                self._board.get_coloring_board())

    def click_on_square(self, x, y):

        if self._board.is_possible_step_at(x, y):
            self.step(x, y)
        else:
            piece = self._current_player.get_piece_at(x, y)

            if piece is None:
                print("No piece selected.")
            else:
                print(f"{piece.get_color().name} {piece.get_type().name} piece at position:"
                      f" x: {piece.get_x()} y: {piece.get_y()} selected by {self._current_player.get_name()}.")
                self.handle_selection(x, y)

    def handle_selection(self, x, y):
        if self._current_player.has_selected_piece() and self._current_player.get_selected_piece().get_coordinates() == (x, y):
            print("Deselected piece.")
            self._current_player.reset_selected_piece()

        elif self._current_player.has_piece_at(x, y):
            print("Selected piece.")
            self._current_player.set_selected_piece(x, y)
            self.get_possible_moves(x, y, self._current_player.get_selected_piece())

        self.update_view()

    def get_possible_moves(self, x, y, piece):
        self._board.update_coloring_board(piece, piece.get_possible_moves(self._board))

    def step(self, x, y):

        print(f"Step made by {self._current_player.get_name()}.")

        # Save the current board state

        moving_piece = self._current_player.get_selected_piece()
        moving_piece.set_coordinates(x, y)
        moving_piece.set_moved()


        # Check if capture
        if self._opponent_player.has_piece_at(x, y):
            print(f"Capture made by {self._current_player.get_name()}.")
            self._opponent_player.remove_piece_at(x, y)
            print(f"{self._opponent_player.get_name()} lost a piece.")
            print(f"{self._opponent_player.get_name()} has {len(self._opponent_player.get_pieces())} pieces.")
            print(f"{self._current_player.get_name()} has {len(self._current_player.get_pieces())} pieces.")

        # Check if promotion

        # Check if castling

        # Check if en passant

        # Check if check

        # Check if checkmate

        # Check if stalemate

        # Switch player
        self._current_player.reset_selected_piece()

        temp = self._current_player
        self._current_player = self._opponent_player
        self._opponent_player = temp

        self.update_view()



    def save_game(self):
        pass

    def load_game(self):
        pass
