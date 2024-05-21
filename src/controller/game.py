from typing import Optional

import numpy as np

from src.controller.custom_types_for_type_hinting import ByteArray8x8
from src.controller.gui_controller import GuiController
from src.model.board import Board
from src.model.enums.enums import Color
from src.model.enums.enums import GameResult
from src.model.enums.enums import PieceType
from src.model.enums.enums import PlayerType
from src.model.pieces.bishop import Bishop
from src.model.pieces.king import King
from src.model.pieces.knight import Knight

from src.model.pieces.pawn import Pawn
from src.model.pieces.queen import Queen
from src.model.pieces.rook import Rook
from src.model.players.player import Player
from src.view.chess_gui import ChessGui

# byte to piece map



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

        self._black_pieces = {(0, 0): Rook(Color.B, 0, 0),
                              (0, 1): Knight(Color.B, 0, 1),
                              (0, 2): Bishop(Color.B, 0, 2),
                              (0, 3): Queen(Color.B, 0, 3),
                              (0, 4): King(Color.B, 0, 4),
                              (0, 5): Bishop(Color.B, 0, 5),
                              (0, 6): Knight(Color.B, 0, 6),
                              (0, 7): Rook(Color.B, 0, 7),
                              (1, 0): Pawn(Color.B, 1, 0),
                              (1, 1): Pawn(Color.B, 1, 1),
                              (1, 2): Pawn(Color.B, 1, 2),
                              (1, 3): Pawn(Color.B, 1, 3),
                              (1, 4): Pawn(Color.B, 1, 4),
                              (1, 5): Pawn(Color.B, 1, 5),
                              (1, 6): Pawn(Color.B, 1, 6),
                              (1, 7): Pawn(Color.B, 1, 7)}

        self._white_pieces = {(7, 0): Rook(Color.W, 7, 0),
                              (7, 1): Knight(Color.W, 7, 1),
                              (7, 2): Bishop(Color.W, 7, 2),
                              (7, 3): Queen(Color.W, 7, 3),
                              (7, 4): King(Color.W, 7, 4),
                              (7, 5): Bishop(Color.W, 7, 5),
                              (7, 6): Knight(Color.W, 7, 6),
                              (7, 7): Rook(Color.W, 7, 7),
                              (6, 0): Pawn(Color.W, 6, 0),
                              (6, 1): Pawn(Color.W, 6, 1),
                              (6, 2): Pawn(Color.W, 6, 2),
                              (6, 3): Pawn(Color.W, 6, 3),
                              (6, 4): Pawn(Color.W, 6, 4),
                              (6, 5): Pawn(Color.W, 6, 5),
                              (6, 6): Pawn(Color.W, 6, 6),
                              (6, 7): Pawn(Color.W, 6, 7)}

        self._selected_piece_position = None
        self._selected_piece = None
        self._possible_fields = None
        self._last_move = None
        self._last_moved_piece = None

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

        last_move = self._last_move
        if self._selected_piece is not None:
            self._selected_piece.update_possible_fields(self._white_pieces.keys(),
                                                        self._black_pieces.keys(),
                                                        self.board)
            # print("White pieces: ", self._white_pieces.keys())
            # print("(0,0)  in White pieces: ", not (7,0) in self._white_pieces.keys())
            possible_fields = self._selected_piece.possible_fields
            # print("Possible fields: ", possible_fields)
        else:
            possible_fields = None
        self._gui_controller.update_board_coloring(self._selected_piece_position,
                                                   possible_fields,
                                                   last_move,
                                                   None)
        # if self.is_white_turn:
        #     checked_king_coordinates = self._current_player.king.coordinates
        # else:
        #     checked_king_coordinates = None

        # print("Board: ", self._board.get_piece_board())
        # print("Coloring: ", self._board.get_coloring_board())

    def bottom_left_button_click(self) -> None:
        self._update_gui()

    def bottom_right_button_click(self) -> None:
        self._update_gui()

    def click_on_board(self, row: int, col: int) -> None:
        print(f"Clicked on: {row}, {col}")
        if not self.is_game_over:
            # A selected piece is clicked -> deselect it
            if self._selected_piece_position == (row, col):
                print("Deselecting the piece.")
                self._selected_piece_position = None
                self._selected_piece = None
                self._update_gui()

            # Own unselected piece is clicked -> select it
            elif self.is_white_turn and (row, col) in self._white_pieces.keys():
                self._selected_piece_position = (row, col)
                self._selected_piece = self._white_pieces[(row, col)]
                print("Selecting white the piece.")
                self._update_gui()

            elif not self.is_white_turn and (row, col) in self._black_pieces.keys():
                self._selected_piece_position = (row, col)
                self._selected_piece = self._black_pieces[(row, col)]
                print("Selecting black the piece.")
                self._update_gui()

            # Selected piece can move to the square -> move it
            if self._selected_piece:
                if (row, col) in self._selected_piece.possible_fields:
                    self.make_move(row, col)
                    print("Making a move.")

            # Empty square or opponent's piece -> deselect the selected piece
            else:
                print("Invalid square.")
                self._selected_piece_position = None
                self._possible_fields = None
                self._update_gui()

    def make_move(self, row: int, col: int):
        # If next_snapshots isn't an empty list that means that we see a previous state, so it is invalid to make a move
        # Or if we'd like to permit the change than the next_snapshots has to be deleted. TODO: decide
        self._make_move(row, col)
        self._selected_piece_position = None
        self.next_turn()

    def _make_move(self, to_row: int, to_col: int) -> None:
        if self._selected_piece is None:
            print("Error: No piece is selected.")

        from_row, from_col = self._selected_piece_position

        # Set is_en_passant field if the pawn moves two squares
        self.reset_en_passant()
        if isinstance(self._selected_piece, Pawn):
            if abs(from_row - to_row) == 2:
                self._selected_piece.is_en_passant = True
                # print("En passant is possible.")

        # Check if the move is a promotion
        if self.is_promotion(to_row):
            piece_type: PieceType = self._gui_controller.get_type_from_promotion_dialog(self._current_player.color)
            self.do_promotion(to_row, to_col, piece_type)
            self.remove_piece_at(from_row, from_col)

        # Check if the move is a castling
        elif self.is_castling(to_col):
            self.do_castling(to_row, to_col)

        # Check if the move is an en passant
        elif self.is_en_passant(to_row, to_col):
            self.do_en_passant(to_row, to_col)
            if self._selected_piece.color == Color.W:
                self._black_pieces.pop((to_row - 1, to_col))
            else:
                self._white_pieces.pop((to_row + 1, to_col))

        # Normal move
        else:
            self.move_piece(to_row, to_col)
            self.remove_piece_at(from_row, from_col)

        self.last_move = (from_row, from_col, to_row, to_col)
        self.last_moved_piece = self._selected_piece

    def remove_piece_at(self, row: int, col: int) -> None:
        if not self.is_white_turn and (row, col) in self._white_pieces.keys():
            self._white_pieces.pop((row, col))
        elif self.is_white_turn and (row, col) in self._black_pieces.keys():
            self._black_pieces.pop((row, col))


    def reset_en_passant(self) -> None:
        if self._last_moved_piece is not None:
            if isinstance(self._last_moved_piece, Pawn):
                self._last_moved_piece.is_en_passant = False

    def is_promotion(self, to_row: int) -> bool:
        return ((to_row == 0) or (to_row == 7)) and self._selected_piece.type == PieceType.PAWN

    def is_en_passant(self, to_row: int, to_col: int) -> bool:
        selected_piece = self._selected_piece
        return (selected_piece.type == PieceType.PAWN and
                to_col != selected_piece.col and
                not self._opponent_player.has_piece_at(to_row, to_col))

    def is_castling(self, to_col: int) -> bool:
        return (self._selected_piece.type == PieceType.KING and
                abs(self._selected_piece.col - to_col) > 1)

    def do_castling(self, to_row: int, to_col: int) -> None:
        print("Castling")

        if to_col == 2:
            rook = self.get_piece_at(row=to_row, col=0)
            if rook is not None:
                rook.coordinates = (to_row, 3)
                rook.is_moved = True
        elif to_col == 6:
            rook = self.get_piece_at(to_row, 7)
            if rook is not None:
                rook.coordinates = (to_row, 5)
                rook.is_moved = True

        king = self.king
        if king is not None:
            king.coordinates = (to_row, to_col)
            king.is_moved = True
        self._last_moved_piece = king
        self.reset_en_passant()
    #
    def do_promotion(self, to_row: int, to_col: int, piece_type: PieceType) -> None:

        from_row, from_col = self.selected_piece.coordinates

        self.remove_piece_at(from_row, from_col)
        if piece_type == PieceType.QUEEN:
            new_piece: Piece = Queen(self.color, to_row, to_col)
        elif piece_type == PieceType.ROOK:
            new_piece = Rook(self.color, to_row, to_col)
        elif piece_type == PieceType.BISHOP:
            new_piece = Bishop(self.color, to_row, to_col)
        elif piece_type == PieceType.KNIGHT:
            new_piece = Knight(self.color, to_row, to_col)
        else:
            raise ValueError("Invalid piece type.")
        self._pieces.append(new_piece)
        self.last_moved_piece = new_piece
        self.reset_en_passant()
    #
    def do_en_passant(self, to_row: int, to_col: int) -> None:
        from_row, from_col = self.selected_piece.coordinates
        self.selected_piece.coordinates = (to_row, to_col)
        self.reset_en_passant()
        self._last_moved_piece = self.selected_piece

    def move_piece(self, to_row: int, to_col: int) -> None:
        from_row, from_col = self.selected_piece.coordinates
        self.selected_piece.coordinates = (to_row, to_col)
        self.selected_piece.is_moved = True
        self._last_moved_piece = self.selected_piece