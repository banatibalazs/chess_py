from src.model.ColorEnum import ColorEnum
import numpy as np

from src.model.Player import Player


class Board:

    def __init__(self, white_player: Player, black_player: Player):
        self._white_player: Player = white_player
        self._black_player: Player = black_player

        self._current_player: Player = self._white_player
        self._opponent_player: Player = self._black_player

        self._selected_piece = None

        self._piece_board = np.zeros((8, 8), dtype=np.byte)
        self._coloring_board = np.zeros((8, 8), dtype=np.str_)

    def is_possible_step_at(self, x, y):
        return self._coloring_board[y][x] == 'P'

    def get_current_player(self):
        return self._current_player

    def update_board(self):
        # After initialization:

        # [[-2,-3,-4,-5,-6,-4,-3,-2],
        #  [-1,-1,-1,-1,-1,-1,-1,-1],
        #  [ 0, 0, 0, 0, 0, 0, 0, 0],
        #  [ 0, 0, 0, 0 ,0 ,0 ,0 ,0],
        #  [ 0, 0, 0, 0, 0, 0, 0, 0],
        #  [ 0, 0, 0, 0, 0, 0, 0, 0],
        #  [ 1, 1, 1, 1, 1, 1, 1, 1],
        #  [ 2, 3, 4, 5, 6, 4, 3, 2]]

        # Reset the board to all 0s
        self._piece_board.fill(0)
        # Update the board with the current piece positions
        self.update_piece_positions(self._white_player.get_pieces())
        self.update_piece_positions(self._black_player.get_pieces())
        # Update the coloring board
        self.update_coloring_board()

    def update_piece_positions(self, pieces):
        for piece in pieces:
            self._piece_board[piece.get_y()][piece.get_x()] = piece.get_type().value * piece.get_color().value

    def reset_coloring_board(self):
        self._coloring_board.fill('O')

    def update_coloring_board(self):

        self._coloring_board.fill('O')
        selected_piece = self._current_player.get_selected_piece()

        if selected_piece is not None:
            x = selected_piece.get_x()
            y = selected_piece.get_y()
            self._coloring_board[y][x] = 'X'

            possible_moves = selected_piece.get_possible_moves(self)
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

    def get_current_player_name(self):
        return self._current_player.get_name()

    def get_opponent_player_name(self):
        return self._opponent_player.get_name()

    def get_opponent_player_piece_number(self):
        return self._opponent_player.get_piece_number()

    def get_current_player_piece_number(self):
        return self._current_player.get_piece_number()

    def get_current_player_color(self):
        return self._current_player.get_color()

    def get_opponent_player_color(self):
        return self._opponent_player.get_color()

    def current_player_has_piece_at(self, x, y):
        return self._current_player.has_piece_at(x, y)

    def opponent_player_has_piece_at(self, x, y):
        return self._opponent_player.has_piece_at(x, y)

    def remove_piece_at(self, x, y):
        if not self._current_player.remove_piece_at(x, y):
            self._opponent_player.remove_piece_at(x, y)

    def switch_players(self):
        # Switch the current player and the opponent player (multiple assignment in Python)
        self._current_player, self._opponent_player = self._opponent_player, self._current_player
        self.reset_selected_piece()

    def get_selected_piece(self):
        return self._selected_piece

    def reset_selected_piece(self):
        self._selected_piece = None

    def has_selected_piece(self):
        return self._selected_piece is not None

    def move_piece(self, piece, x, y):
        pass

    def remove_piece(self, piece):
        pass

    def set_selected_piece(self, x, y):
        if self.has_piece_at(x, y):
            self._selected_piece = self._get_piece_at(x, y)

    def _get_piece_at(self, x, y):
        if self._current_player.has_piece_at(x, y):
            return self._current_player.get_piece_at(x, y)
        elif self._opponent_player.has_piece_at(x, y):
            return self._opponent_player.get_piece_at(x, y)
        else:
            return None

    def has_piece_at(self, x, y):
        return self._piece_board[y][x] != 0


