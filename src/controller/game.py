from typing import Optional, Tuple, Set

import numpy as np

from src.controller.custom_types_for_type_hinting import ByteArray8x8
from src.controller.gui_controller import GuiController
from src.model.enums.enums import Color
from src.model.enums.enums import PieceType
from src.model.enums.enums import PlayerType
from src.model.pieces.piece import Piece
from src.view.chess_gui import ChessGui
from src.model.pieces.piece_logics import PieceLogics



class Game:
    def __init__(self, title: str, white_player_name: str, white_player_type: PlayerType, black_player_name: str,
                 black_player_type: PlayerType, _time: Optional[int], pov: Color) -> None:

        self.gui: ChessGui = ChessGui(title, pov, white_player_name, black_player_name, _time,
                                      self.click_on_board, self.bottom_right_button_click,
                                      self.bottom_left_button_click)

        self._gui_controller: GuiController = GuiController(self.gui)

        self.board: ByteArray8x8 = np.array([
            [-2, -3, -4, -5, -6, -4, -3, -2],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0,  0,  0,  0,  0,  0,  0,  0],
            [0,  0,  0,  0,  0,  0,  0,  0],
            [0,  0,  0,  0,  0,  0,  0,  0],
            [0,  0,  0,  0,  0,  0,  0,  0],
            [1,  1,  1,  1,  1,  1,  1,  1],
            [2,  3,  4,  5,  6,  4,  3,  2]], dtype=np.byte)

        self._white_king_coordinates = np.where(self.board == 6)
        self._black_king_coordinates = np.where(self.board == -6)

        self.step_from: Optional[Tuple[int, int]] = None
        self.step_to: Optional[Tuple[int, int]] = None

        self._selected_piece_code: Optional[int] = None
        self._possible_fields: Set[Tuple[int, int]] = set()

        self._last_move = None
        self._last_moved_piece = None

        # black king
        self._king_04_is_moved = False
        # white king
        self._king_74_is_moved = False
        # black rooks
        self._rook_00_is_moved = False
        self._rook_07_is_moved = False
        # white rooks
        self._rook_70_is_moved = False
        self._rook_77_is_moved = False

        self._is_en_passant = False

        self.is_white_turn: bool = True
        self.is_game_over: bool = False

        self.start_game()

    def start_game(self) -> None:
        self._update_gui()

    def next_turn(self) -> None:
        self.is_white_turn = not self.is_white_turn
        self._update_gui()

    def _update_gui(self) -> None:
        self._gui_controller.update_pieces_on_board(self.board)

        self._gui_controller.update_board_coloring(self.step_from,
                                                   self._possible_fields,
                                                   self._last_move,
                                                   None)
        # print("Board: ", self._board.get_piece_board())

    def bottom_left_button_click(self) -> None:
        self._update_gui()

    def bottom_right_button_click(self) -> None:
        self._update_gui()

    def click_on_board(self, row: int, col: int) -> None:
        # print(f"Clicked on: {row}, {col}")
        if not self.is_game_over:
            # A selected piece is clicked -> deselect it
            if self.step_from == (row, col):
                # print("Deselecting the piece.")
                self.step_from = None
                self._update_gui()

            # Own unselected piece is clicked -> select it
            elif (self.is_white_turn and self.board[row, col] > 0 or
                  not self.is_white_turn and self.board[row, col] < 0):
                self.step_from = (row, col)
                self.get_possible_fields()
                # print("Selecting white the piece.")
                self._update_gui()

            # Selected piece can move to the square -> move it
            if self.step_from:
                if (row, col) in self._possible_fields:
                    self.step_to = (row, col)
                    self.make_move()
                    # print("Making a move.")

            # Empty square or opponent's piece -> deselect the selected piece
            else:
                print("Invalid square.")
                self._possible_fields = set()
                self._update_gui()

    def make_move(self):
        # If next_snapshots isn't an empty list that means that we see a previous state, so it is invalid to make a move
        # Or if we'd like to permit the change than the next_snapshots has to be deleted. TODO: decide
        self._make_move()
        self.next_turn()

    def _make_move(self) -> None:
        if self.step_from is None or self.step_to is None:
            return

        from_row, from_col = self.step_from
        to_row, to_col = self.step_to
        color = Color.W if self.is_white_turn else Color.B
        piece = self.board[from_row, from_col]

        if piece == -6:
            self._king_04_is_moved = True
        elif piece == 6:
            self._king_74_is_moved = True
        elif piece == -2:
            if self.step_from == (0, 0):
                self._rook_00_is_moved = True
            elif self.step_from == (0, 7):
                self._rook_07_is_moved = True
        elif piece == 2:
            if self.step_from == (7, 0):
                self._rook_70_is_moved = True
            elif self.step_from == (7, 7):
                self._rook_77_is_moved = True

        # Set is_en_passant field if the pawn moves two squares
        self._is_en_passant = False
        if abs(self.board[from_row, from_col]) == 1:
            if abs(from_row - to_row) == 2:
                self._is_en_passant = True
                print("En passant is possible.")

        # Check if the move is a promotion
        if self.is_promotion(to_row, piece):
            piece = self._gui_controller.get_type_from_promotion_dialog(color) # TODO change this
            self.do_promotion(from_row, from_col, to_row, to_col, piece)
            # self.board[to_row, to_col] = 0

        # Check if the move is a castling
        elif self.is_castling(from_col, to_col, piece):
            self.do_castling(from_row, from_col, to_row, to_col)

        # Check if the move is an en passant
        elif self.is_en_passant(from_col, to_row, to_col, piece):
            print("En passant")
            self.board[from_row, from_col] = 0
            self.board[to_row, to_col] = piece
            if color == Color.W:
                self.board[to_row + 1, to_col] = 0
            else:
                self.board[to_row - 1, to_col] = 0

        # Normal move
        else:
            self.board[from_row, from_col] = 0
            self.board[to_row, to_col] = piece

        self._last_move = (from_row, from_col, to_row, to_col)
        self.last_moved_piece = piece
        self._possible_fields.clear()
        self.step_from = None

    def is_promotion(self, to_row: int, piece) -> bool:
        return ((to_row == 0) or (to_row == 7)) and abs(piece) == 1

    def is_en_passant(self, from_col: int, to_row: int, to_col: int, piece) -> bool:
        print("Is en passant function.")
        if self.is_white_turn:
            return (abs(piece) == 1 and
                    to_col != from_col and
                    not self.board[to_row, to_col] > 0)
        else:
            return (abs(piece) == 1 and
                    to_col != from_col and
                    not self.board[to_row, to_col] < 0)

    def is_castling(self, from_col: int, to_col: int, piece) -> bool:
        return abs(piece) == 6 and abs(from_col - to_col) > 1

    def do_castling(self, from_row: int, from_col: int, to_row: int, to_col: int) -> None:
        print("Castling")

        if to_col == 2:
            rook = self.board[to_row, 0]
            if abs(rook) == 2:
                self.board[to_row, 0] = 0
                self.board[to_row, 3] = rook
                # rook.is_moved = True TODO
        elif to_col == 6:
            rook = self.board[to_row, 7]
            if abs(rook) == 2:
                self.board[to_row, 7] = 0
                self.board[to_row, 5] = rook
                # rook.is_moved = True TODO

        king = self.board[from_row, from_col]
        self.board[from_row, from_col] = 0
        self.board[to_row, to_col] = king
        # king.is_moved = True TODO

    def do_promotion(self, from_row, from_col, to_row: int, to_col: int, piece_type: int) -> None:
        print("Promotion")
        self.board[from_row, from_col] = 0
        self.board[to_row, to_col] = piece_type

    def get_possible_fields(self) -> None:
        self._possible_fields = PieceLogics.get_possible_fields(self.board, self.step_from,
                                                                self._king_04_is_moved, self._king_74_is_moved,
                                                                self._rook_00_is_moved, self._rook_07_is_moved,
                                                                self._rook_70_is_moved, self._rook_77_is_moved,
                                                                self._is_en_passant, self._last_move)
