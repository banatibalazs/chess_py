from typing import Optional, Tuple, Set
import numpy as np
from src.controller.custom_types_for_type_hinting import ByteArray8x8
from src.controller.gui_controller import GuiController
from src.model.utility.enums import Color, GameResult
from src.model.utility.enums import PlayerType
from src.view.chess_gui import ChessGui
from src.model.pieces.piece_logics import PieceLogics
import time

import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to execute.")
        return result
    return wrapper


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
        self.check_if_game_over()

    def check_if_game_over(self) -> None:
        if self.is_white_turn:
            possible_moves = PieceLogics.get_all_possible_moves(self.board, True, self._king_04_is_moved,
                                                                self._king_74_is_moved, self._rook_00_is_moved,
                                                                self._rook_07_is_moved, self._rook_70_is_moved,
                                                                self._rook_77_is_moved, self._is_en_passant,
                                                                self._last_move)
        else:
            possible_moves = PieceLogics.get_all_possible_moves(self.board, False, self._king_04_is_moved,
                                                                self._king_74_is_moved, self._rook_00_is_moved,
                                                                self._rook_07_is_moved, self._rook_70_is_moved,
                                                                self._rook_77_is_moved, self._is_en_passant,
                                                                self._last_move)
        print(f"All possible moves: {possible_moves}")
        if len(possible_moves) == 0:
            if self.is_white_turn:
                self.end_game(GameResult.BLACK_WON_BY_CHECKMATE)
            else:
                self.end_game(GameResult.WHITE_WON_BY_CHECKMATE)

    def end_game(self, game_result: GameResult) -> None:
        self.is_game_over = True
        self._gui_controller.end_game_dialog(game_result)

    def _update_gui(self) -> None:
        self._gui_controller.update_pieces_on_board(self.board)

        self._gui_controller.update_board_coloring(self.step_from,
                                                   self._possible_fields,
                                                   self._last_move,
                                                   self.get_checked_king_coordinates())
        # print("Board: ", self._board.get_piece_board())

    def get_checked_king_coordinates(self) -> Optional[Tuple[int, int]]:
        attacked_fields = PieceLogics.get_opponents_attacked_fields(self.board, self.is_white_turn)
        if self.is_white_turn:
            king_coordinates = tuple(np.argwhere(self.board == 6)[0])
        else:
            king_coordinates = tuple(np.argwhere(self.board == -6)[0])

        if king_coordinates in attacked_fields:
            return king_coordinates
        return None

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

    def make_move(self) -> None:
        if self.step_from is None or self.step_to is None:
            return

        from_row, from_col = self.step_from
        to_row, to_col = self.step_to
        color = Color.W if self.is_white_turn else Color.B
        piece = self.board[from_row, from_col]

        # Set is_moved flags for kings and rooks
        self.set_is_moved_flags(piece)

        # Set is_en_passant field if the pawn moves two squares
        self._is_en_passant = False
        if abs(self.board[from_row, from_col]) == 1:
            if abs(from_row - to_row) == 2:
                self._is_en_passant = True
                print("Is_en_passant variable is set to True.")

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

        self.next_turn()

    def set_is_moved_flags(self, piece) -> None:
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

    def is_promotion(self, to_row: int, piece) -> bool:
        return ((to_row == 0) or (to_row == 7)) and abs(piece) == 1

    def is_en_passant(self, from_col: int, to_row: int, to_col: int, piece) -> bool:
        print("Is en passant function.")
        print("Is en passant: ", self._is_en_passant)
        if self._last_move is None:
            return False
        last_from_row, last_from_col, last_to_row, last_to_col = self._last_move
        if self.is_white_turn:
            return (abs(last_from_row - last_to_row) > 1 and abs(piece) == 1 and
                    to_col != from_col and
                    not self.board[to_row, to_col] > 0 and self.board[to_row + 1, to_col] < 0)
        else:
            return (abs(last_from_row - last_to_row) > 1 and abs(piece) == 1 and
                    to_col != from_col and
                    not self.board[to_row, to_col] < 0 and self.board[to_row - 1, to_col] > 0)

    def is_castling(self, from_col: int, to_col: int, piece) -> bool:
        return abs(piece) == 6 and abs(from_col - to_col) > 1

    def do_castling(self, from_row: int, from_col: int, to_row: int, to_col: int) -> None:
        print("Castling")

        if to_col == 2:
            rook = self.board[to_row, 0]
            if abs(rook) == 2:
                self.board[to_row, 0] = 0
                self.board[to_row, 3] = rook
        elif to_col == 6:
            rook = self.board[to_row, 7]
            if abs(rook) == 2:
                self.board[to_row, 7] = 0
                self.board[to_row, 5] = rook

        if to_row == 0:
            if to_col == 2:
                self._rook_00_is_moved = True
            elif to_col == 6:
                self._rook_07_is_moved = True
        elif to_row == 7:
            if to_col == 2:
                self._rook_70_is_moved = True
            elif to_col == 6:
                self._rook_77_is_moved = True

        king = self.board[from_row, from_col]
        self.board[from_row, from_col] = 0
        self.board[to_row, to_col] = king
        # king.is_moved = True TODO

    def do_promotion(self, from_row, from_col, to_row: int, to_col: int, piece_type: int) -> None:
        print("Promotion")
        self.board[from_row, from_col] = 0
        self.board[to_row, to_col] = piece_type

    def get_possible_fields(self) -> None:
        self._possible_fields = PieceLogics.get_possible_moves_of_piece(self.board, self.step_from,
                                                                        self._king_04_is_moved, self._king_74_is_moved,
                                                                        self._rook_00_is_moved, self._rook_07_is_moved,
                                                                        self._rook_70_is_moved, self._rook_77_is_moved,
                                                                        self._is_en_passant, self._last_move)
