from src.model.ColorEnum import ColorEnum


class Board:

    def __init__(self, white_pieces, black_pieces):

        self._piece_board = [[0 for _ in range(8)] for _ in range(8)]
        self._white_attack_board = [[0 for _ in range(8)] for _ in range(8)]
        self._black_attack_board = [[0 for _ in range(8)] for _ in range(8)]
        self._selected_piece = None
        self._coloring_board = [['O' for _ in range(8)] for _ in range(8)]
        self._possible_moves = [[0 for _ in range(8)] for _ in range(8)]
        self.update_board(white_pieces, black_pieces)

    def update_board(self, white_pieces, black_pieces):
        # Create a 2D array representing the board with the pieces
        # After initialization:

        # [[-2,-3,-4,-5,-6,-4,-3,-2],
        #  [-1,-1,-1,-1,-1,-1,-1,-1],
        #  [ 0, 0, 0, 0, 0, 0, 0, 0],
        #  [ 0, 0, 0, 0 ,0 ,0 ,0 ,0],
        #  [ 0, 0, 0, 0, 0, 0, 0, 0],
        #  [ 0, 0, 0, 0, 0, 0, 0, 0],
        #  [ 1, 1, 1, 1, 1, 1, 1, 1],
        #  [ 2, 3, 4, 5, 6, 4, 3, 2]]
        self.update_piece_positions(white_pieces)
        self.update_piece_positions(black_pieces)
        self.update_coloring_board()

    def update_coloring_board(self, selected_piece=None):

        self._coloring_board = [['O' for _ in range(8)] for _ in range(8)]

        if selected_piece is not None:
            self._coloring_board[selected_piece.get_x()][selected_piece.get_y()] = 'X'

    def update_piece_positions(self, pieces):
        for piece in pieces:
            self._piece_board[piece.get_x()][piece.get_y()] = piece.get_type().value * piece.get_color().value

    def get_value_at(self, x, y):
        # Get the value of the piece at the given coordinates
        return self._piece_board[x][y]

    def get_color_at(self, x, y):
        # Get the color of the piece at the given coordinates
        if self._piece_board[x][y] < 0:
            return ColorEnum.BLACK
        elif self._piece_board[x][y] > 0:
            return ColorEnum.WHITE
        else:
            return ColorEnum.NONE

    def get_possible_squares(self):
        return self._possible_moves

    def get_coloring_board(self):
        return self._coloring_board

    def get_piece_board(self):
        return self._piece_board

    def get_piece_at(self, x, y, is_white):
        pass

    def get_selected_piece(self):
        pass

    def move_piece(self, piece, x, y):
        pass

    def remove_piece(self, piece):
        pass
