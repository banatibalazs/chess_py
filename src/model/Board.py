from src.model.ColorEnum import ColorEnum


class Board:

    def __init__(self, white_pieces, black_pieces):

        self._piece_board = [[0 for _ in range(8)] for _ in range(8)]
        self._white_attack_board = [[0 for _ in range(8)] for _ in range(8)]
        self._black_attack_board = [[0 for _ in range(8)] for _ in range(8)]
        self._coloring_board = [['O' for _ in range(8)] for _ in range(8)]

    def is_possible_step_at(self, x, y):
        return self._coloring_board[y][x] == 'P'

    def update_board(self, white_pieces, black_pieces):
        # After initialization:

        # [[-2,-3,-4,-5,-6,-4,-3,-2],
        #  [-1,-1,-1,-1,-1,-1,-1,-1],
        #  [ 0, 0, 0, 0, 0, 0, 0, 0],
        #  [ 0, 0, 0, 0 ,0 ,0 ,0 ,0],
        #  [ 0, 0, 0, 0, 0, 0, 0, 0],
        #  [ 0, 0, 0, 0, 0, 0, 0, 0],
        #  [ 1, 1, 1, 1, 1, 1, 1, 1],
        #  [ 2, 3, 4, 5, 6, 4, 3, 2]]

        self._piece_board = [[0 for _ in range(8)] for _ in range(8)]
        self.update_piece_positions(white_pieces)
        self.update_piece_positions(black_pieces)
        self.update_coloring_board()

    def update_piece_positions(self, pieces):
        for piece in pieces:
            self._piece_board[piece.get_y()][piece.get_x()] = piece.get_type().value * piece.get_color().value

    def reset_coloring_board(self):
        self._coloring_board = [['O' for _ in range(8)] for _ in range(8)]

    def update_coloring_board(self, selected_piece=None, possible_moves=None):

        self._coloring_board = [['O' for _ in range(8)] for _ in range(8)]

        if selected_piece is not None:
            self._coloring_board[selected_piece.get_y()][selected_piece.get_x()] = 'X'
        if possible_moves is not None:
            for move in possible_moves:
                self._coloring_board[move[1]][move[0]] = 'P'

    def get_value_at(self, x, y):
        # Get the value of the piece at the given coordinates
        return self._piece_board[y][x]

    def get_color_at(self, x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return ColorEnum.NONE
        # Get the color of the piece at the given coordinates
        if self._piece_board[y][x] < 0:
            return ColorEnum.BLACK
        elif self._piece_board[y][x] > 0:
            return ColorEnum.WHITE
        else:
            return ColorEnum.NONE

    def is_empty(self, x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        return self.get_value_at(x, y) == 0

    def is_enemy(self, x, y, color):
        return self.get_color_at(x, y) != color and self.get_color_at(x, y) != ColorEnum.NONE

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
