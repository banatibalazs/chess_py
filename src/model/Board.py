from src.model.ColorEnum import ColorEnum
from src.model.Player import Player


class Board:

    def __init__(self, white_player_name, black_player_name):

        self._white_player = Player(white_player_name, ColorEnum.WHITE)
        self._black_player = Player(black_player_name, ColorEnum.BLACK)
        self._int_board = []

        self.update_int_board()
        self.print_board()

    def print_board(self):
        for row in self._int_board:
            for square in row:
                print("[", str(square).center(4), end="]")
            print("\n")

    def get_int_board(self):
        return self._int_board

    def update_int_board(self):
        # Create a 2D array representing the board with the pieces
        # The array will contain the value of the piece at the given coordinates
        # After initialization:

        # [[-2,-3,-4,-5,-6,-4,-3,-2],
        #  [-1,-1,-1,-1,-1,-1,-1,-1],
        #  [ 0, 0, 0, 0, 0, 0, 0, 0],
        #  [ 0, 0, 0, 0 ,0 ,0 ,0 ,0],
        #  [ 0, 0, 0, 0, 0, 0, 0, 0],
        #  [ 0, 0, 0, 0, 0, 0, 0, 0],
        #  [ 1, 1, 1, 1, 1, 1, 1, 1],
        #  [ 2, 3, 4, 5, 6, 4, 3, 2]]

        self._int_board = [[0 for _ in range(8)] for _ in range(8)]
        for piece in self._white_player.get_pieces():
            self._int_board[piece.get_x()][piece.get_y()] = piece.get_type().value * piece.get_color().value
        for piece in self._black_player.get_pieces():
            self._int_board[piece.get_x()][piece.get_y()] = piece.get_type().value * piece.get_color().value

    def get_value_at(self, x, y):
        # Get the value of the piece at the given coordinates
        return self._int_board[x][y]

    def get_piece_at(self, x, y, is_white):
        pass

    def get_selected_piece(self):
        pass

    def move_piece(self, piece, x, y):
        pass

    def remove_piece(self, piece):
        pass
