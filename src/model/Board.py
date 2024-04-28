from typing import Optional

from src.controller.CustomTypesForTypeHinting import ByteArray8x8, CharArray8x8
from src.model.ColorEnum import ColorEnum
import numpy as np

from src.model.Rook import Rook
from src.model.King import King
from src.model.Pawn import Pawn
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum
from src.model.Player import Player


class Board:

    NORMAL_MOVE_SYMBOL = b'n'
    SPECIAL_MOVE_SYMBOL = b's'
    SELECTED_PIECE_SYMBOL = b'x'
    EMPTY_SYMBOL = b'o'

    def __init__(self, white_player: Player, black_player: Player):
        self._white_player: Player = white_player
        self._black_player: Player = black_player

        self._current_player: Player = self._white_player
        self._opponent_player: Player = self._black_player

        self._selected_piece: Optional[Piece] = None

        self._piece_board = np.zeros((8, 8), dtype=np.byte)
        self._coloring_board = np.zeros((8, 8), dtype=np.character)

        self._white_attack_board = np.zeros((8, 8), dtype=np.bool_)
        self._black_attack_board = np.zeros((8, 8), dtype=np.bool_)

    def is_normal_move_at(self, x, y):
        return self._coloring_board[y, x] == self.NORMAL_MOVE_SYMBOL

    def is_special_move_at(self, x, y):
        return self._coloring_board[y, x] == self.SPECIAL_MOVE_SYMBOL

    def update_board(self):
        # Reset the board to all 0s
        self._piece_board.fill(0)
        # Update the board with the current piece positions
        self.update_piece_positions(self._white_player.get_pieces())
        self.update_piece_positions(self._black_player.get_pieces())
        # Update the coloring board
        self.update_coloring_board()

    @staticmethod
    def update_board_after(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.update_board()
            return result

        return wrapper

    def update_piece_positions(self, pieces):
        for piece in pieces:
            self._piece_board[piece.y][piece.x] = piece.type.value * piece.color.value

    def update_coloring_board(self):

        self._coloring_board.fill(self.EMPTY_SYMBOL)

        if self._selected_piece is not None:
            x = self._selected_piece.x
            y = self._selected_piece.y
            self._coloring_board[y, x] = self.SELECTED_PIECE_SYMBOL

            possible_moves = self._selected_piece.get_possible_moves(self)
            if possible_moves is not None:
                for move in possible_moves:
                    self._coloring_board[move[1], move[0]] = self.NORMAL_MOVE_SYMBOL

        if isinstance(self._selected_piece, King):
            self.check_castling()

    def check_castling(self):

        '''
                The board [yx] coordinates                               Piece codes
                                                                        Black player

                [00][01][02][03][04][05][06][07]            [-2][-3][-4][-5][-6][-4][-3][-2]
                [10][11][12][13][14][15][16][17]            [-1][-1][-1][-1][-1][-1][-1][-1]
                [20][21][22][23][24][25][26][27]            [ 0][ 0][ 0][ 0][ 0][ 0][ 0][ 0]
                [30][31][32][33][34][35][36][37]            [ 0][ 0][ 0][ 0][ 0][ 0][ 0][ 0]
                [40][41][42][43][44][45][46][47]            [ 0][ 0][ 0][ 0][ 0][ 0][ 0][ 0]
                [50][51][52][53][54][55][56][57]            [ 0][ 0][ 0][ 0][ 0][ 0][ 0][ 0]
                [60][61][62][63][64][65][66][67]            [ 1][ 1][ 1][ 1][ 1][ 1][ 1][ 1]
                [70][71][72][73][74][75][76][77]            [ 2][ 3][ 4][ 5][ 6][ 4][ 3][ 2]

                                                                        White player
                '''

        self.update_attack_boards()

        if self._current_player.get_color() == ColorEnum.BLACK:
            # Then king is at (4, 0) and rooks are at (0, 0) and (7, 0)
            king = self._current_player.get_piece_at(4, 0)
            rook = self._current_player.get_piece_at(0, 0)
            if (isinstance(rook, Rook) and
                isinstance(king, King) and
                not rook.is_moved() and
                not king.is_moved() and
                self.is_empty_at(1, 0) and
                self.is_empty_at(2, 0) and
                self.is_empty_at(3, 0) and
                not self.square_is_attacked_by_black(4, 0) and
                not self.square_is_attacked_by_white(4, 0) and
                not self.square_is_attacked_by_white(3, 0) and
                not self.square_is_attacked_by_white(2, 0)):
                self._coloring_board[0, 2] = self.SPECIAL_MOVE_SYMBOL

            rook = self._current_player.get_piece_at(7, 0)
            if (isinstance(rook, Rook) and
                isinstance(king, King) and
                not rook.is_moved() and
                not king.is_moved() and
                self.is_empty_at(5, 0) and
                self.is_empty_at(6, 0) and
                not self.square_is_attacked_by_black(4, 0) and
                not self.square_is_attacked_by_white(4, 0) and
                not self.square_is_attacked_by_white(5, 0) and
                not self.square_is_attacked_by_white(6, 0)):
                self._coloring_board[0, 6] = self.SPECIAL_MOVE_SYMBOL

        else:
            king = self._current_player.get_piece_at(4, 7)
            rook = self._current_player.get_piece_at(0, 7)
            if (isinstance(rook, Rook) and
                isinstance(king, King) and
                not rook.is_moved() and
                not king.is_moved() and
                self.is_empty_at(1, 7) and
                self.is_empty_at(2, 7) and
                self.is_empty_at(3, 7) and
                not self.square_is_attacked_by_white(4, 7) and
                not self.square_is_attacked_by_black(4, 7) and
                not self.square_is_attacked_by_black(3, 7) and
                not self.square_is_attacked_by_black(2, 7)):
                self._coloring_board[7, 2] = self.SPECIAL_MOVE_SYMBOL

            rook = self._current_player.get_piece_at(7, 7)
            if (isinstance(rook, Rook) and
                isinstance(king, King) and
                not rook.is_moved() and
                not king.is_moved() and
                self.is_empty_at(5, 7) and
                self.is_empty_at(6, 7) and
                not self.square_is_attacked_by_white(4, 7) and
                not self.square_is_attacked_by_black(4, 7) and
                not self.square_is_attacked_by_black(5, 7) and
                not self.square_is_attacked_by_black(6, 7)):
                self._coloring_board[7, 6] = self.SPECIAL_MOVE_SYMBOL



    def square_is_attacked_by_white(self, x, y) -> bool:
        return self._white_attack_board[y, x]

    def square_is_attacked_by_black(self, x, y) -> bool:
        return self._black_attack_board[y, x]

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

    def get_coloring_board(self) -> CharArray8x8:
        return self._coloring_board

    def get_piece_board(self) -> ByteArray8x8:
        return self._piece_board

    @property
    def current_player_name(self):
        return self._current_player.get_name()

    @property
    def white_player_piece_number(self) -> int:
        return self._white_player.get_piece_number()

    @property
    def black_player_piece_number(self) -> int:
        return self._black_player.get_piece_number()

    @property
    def opponent_player_piece_number(self) -> int:
        return self._opponent_player.get_piece_number()

    @property
    def current_player_piece_number(self) -> int:
        return self._current_player.get_piece_number()

    def is_friend_at(self, x: int, y: int) -> bool:
        return self._current_player.has_piece_at(x, y)

    def is_opponent_at(self, x: int, y: int) -> bool:
        return self._opponent_player.has_piece_at(x, y)

    def switch_players(self) -> None:
        # Switch the current player and the opponent player (multiple assignment in Python)
        self._current_player, self._opponent_player = self._opponent_player, self._current_player
        self.reset_selected_piece()

    @update_board_after
    def reset_selected_piece(self) -> None:
        self._selected_piece = None

    @update_board_after
    def select_piece_at(self, x: int, y: int) -> None:
        if self._current_player.has_piece_at(x, y):
            self._selected_piece = self._current_player.get_piece_at(x, y)

    def is_empty_at(self, x: int, y: int) -> bool:
        return self._piece_board[y][x] == 0

    @property
    def selected_piece_coordinate_x(self) -> int:
        return self._selected_piece.x

    @property
    def selected_piece_coordinate_y(self) -> int:
        return self._selected_piece.y

    def is_selected_piece_at(self, x: int, y: int) -> bool:
        return self._coloring_board[y, x] == self.SELECTED_PIECE_SYMBOL

    def move_piece_to(self, to_x: int, to_y: int) -> None:
        piece = self._selected_piece
        from_x, from_y = piece.coordinates

        # Pawn specific rules and checks
        if isinstance(piece, Pawn):

            # Pawn promotion
            if to_y == 0 or to_y == 7:
                self._current_player.promote_pawn(from_x, from_y, to_x, to_y, PieceTypeEnum.QUEEN)

            # Set en passant field if the pawn moves two squares
            if abs(from_y - to_y) == 2:
                self._selected_piece.set_en_passant(True)


        '''
        Castling rules
        
        1. Neither the king nor the rook has previously moved.
        2. There are no pieces between the king and the rook.
        3. The king is not currently in check.
        4. The king does not pass through or finish on a square that is attacked by an enemy piece.
        
                        (x, y)
        Rook positions: (0, 0), (7, 0), (0, 7), (7, 7)
        King positions: (4, 0), (4, 7)
        '''

        if isinstance(self._selected_piece, King) and not piece.is_moved():
            if to_x == 6 and to_y == 0:
                self._current_player.castling(4, 0, 7, 0)
            elif to_x == 2 and to_y == 0:
                self._current_player.castling(4, 0, 0, 0)
            elif to_x == 6 and to_y == 7:
                self._current_player.castling(4, 7, 7, 7)
            elif to_x == 2 and to_y == 7:
                self._current_player.castling(4, 7, 0, 7)


        self._selected_piece.set_coordinates(to_x, to_y)
        self.capture_piece_at(to_x, to_y)
        self._selected_piece.set_moved()

        self.switch_players()

        # reset en passant

    def check_en_passant(self, x: int, y: int) -> bool:
        pass

    @update_board_after
    def capture_piece_at(self, x: int, y: int) -> None:
        if self._opponent_player.has_piece_at(x, y):
            self._opponent_player.remove_piece_at(x, y)

    def update_attack_boards(self) -> None:
        self._white_attack_board.fill(False)
        self._black_attack_board.fill(False)

        for player, attack_board in [(self._white_player, self._white_attack_board),
                                     (self._black_player, self._black_attack_board)]:
            for piece in player.get_pieces():
                attacked_locations = piece.get_attacked_locations(self) if isinstance(piece,
                          Pawn) else piece.get_possible_moves(self)
                for location in attacked_locations:
                    attack_board[location[1], location[0]] = True

    def get_black_attack_board(self):
        return self._black_attack_board

    def get_white_attack_board(self):
        return self._white_attack_board

    def is_attacked_by_white_at(self, x: int, y: int):
        return self._white_attack_board[y, x]

    def is_attacked_by_black_at(self, x: int, y: int):
        return self._black_attack_board[y, x]

    # def get_opponent_attack_board(self):
    #     return self._opponent_player.get_attack_board(self)

    def is_en_passant(self, x: int, y: int) -> bool:
        if self.get_piece_at(x, y) is not None:
            if isinstance(self.get_piece_at(x, y), Pawn):
                return self.get_piece_at(x, y).is_en_passant

    def get_piece_at(self, x: int, y: int) -> Optional[Piece]:
        if self._current_player.has_piece_at(x, y):
            return self._current_player.get_piece_at(x, y)
        else:
            return self._opponent_player.get_piece_at(x, y)



