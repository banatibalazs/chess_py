import time
from typing import List, Optional
from src.controller.Snapshot import Snapshot
from src.controller.GuiController import GuiController
from src.controller.StepHistory import StepHistory
from src.controller.TimerThread import TimerThread
from src.model.Board import Board
from src.model.Color import Color
from src.model.ComputerPlayer import ComputerPlayer
from src.model.GameResult import GameResult
from src.model.Pawn import Pawn
from src.model.PieceType import PieceType
from src.model.Player import Player
from src.view.ChessGui import ChessGui


class Game:
    def __init__(self, title: str, white_player_name: str, white_is_ai: bool, black_player_name: str, black_is_ai: bool,
                 time: Optional[int]) -> None:

        self.gui: ChessGui = ChessGui(title, white_player_name, black_player_name, time,
                                      self.click_on_board, self.top_left_button_click,
                                      self.top_right_button_click, self.bottom_right_button_click,
                                      self.bottom_left_button_click)
        if time is None:
            self.timer = None
        else:
            self.timer = TimerThread(self)

        self._gui_controller: GuiController = GuiController(self.gui)

        self._board: Board = Board()
        if white_is_ai:
            self._white_player: Player = ComputerPlayer(white_player_name, Color.WHITE, self._board, time)
        else:
            self._white_player: Player = Player(white_player_name, Color.WHITE, self._board, time)
        if black_is_ai:
            self._black_player: Player = ComputerPlayer(black_player_name, Color.BLACK, self._board, time)
        else:
            self._black_player: Player = Player(black_player_name, Color.BLACK, self._board, time)
        self._current_player: Player = self._white_player
        self._opponent_player: Player = self._black_player

        self.is_white_turn: bool = True
        self.is_game_over: bool = False

        self.step_history: StepHistory = StepHistory()
        self.snapshots: List[Snapshot] = []
        self.current_snapshot_index = 0

        self.start_game()

    def __del__(self):
        if self.timer is not None:
            self.timer.stop()
        # self.gui.destroy()
        print("Game destroyed.")

    def start_game(self) -> None:
        self._white_player.init_pieces()
        self._black_player.init_pieces()

        if self.timer is not None:
            self.timer.start()

        self.save_snapshot()
        self._update_player()
        self._update_board()
        self._update_gui()

        if isinstance(self._current_player, ComputerPlayer):
            self._current_player.select_piece()
            move = self._current_player.choose_move()
            self.make_move(move[0], move[1])

    def next_turn(self) -> None:
        self.is_white_turn = not self.is_white_turn
        self._current_player, self._opponent_player = self._opponent_player, self._current_player
        self.save_snapshot()
        self._update_player()
        if self._current_player.can_move():
            if len(self._current_player.pieces) == 1 and len(self._opponent_player.pieces) == 1:
                print("Draw: Only two kings left.")
                self.end_game(GameResult.DRAW)
        else:
            if self._current_player.king.is_in_check:
                print(f"Checkmate: {self._current_player.color.name} {self._current_player.name} can't move.")
                self.end_game(GameResult.WHITE_WON_BY_CHECKMATE if
                              self._current_player.color == Color.BLACK else GameResult.BLACK_WON_BY_CHECKMATE)
            else:
                print(f"{self._current_player.name} can't move.")
                self.end_game(GameResult.DRAW)

        if not self.is_game_over and isinstance(self._current_player, ComputerPlayer):
            self._current_player.select_piece()
            move = self._current_player.choose_move()
            self.make_move(move[0], move[1])


    def end_game(self, game_result: GameResult) -> None:
        self.is_game_over = True
        if self.timer is not None:
            self.timer.stop()
        self._update_board()
        self._update_gui()
        self._gui_controller.end_game_dialog(game_result)

    def threefold_repetition(self) -> bool:
        # TODO implement
        pass

    def time_out(self, color: Color) -> None:
        print(f"Time out: {color.name} {self._current_player.name} ran out of time.")
        self.end_game(GameResult.WHITE_WON_BY_TIMEOUT if color == Color.BLACK else GameResult.BLACK_WON_BY_TIMEOUT)

    def _update_gui(self) -> None:
        self._gui_controller.update_pieces_on_board(self._board.get_piece_board())

        coordinates = None
        possible_fields = None

        if self._current_player.selected_piece is not None:
            coordinates = self._current_player.selected_piece.coordinates
            possible_fields = self._current_player.selected_piece.possible_fields

        last_move = self._opponent_player.last_move
        if self._current_player.king.is_in_check:
            checked_king_coordinates = self._current_player.king.coordinates
        else:
            checked_king_coordinates = None
        self._gui_controller.update_board_coloring(coordinates, possible_fields, last_move, checked_king_coordinates)
        self._gui_controller.update_labels(str(self._white_player.get_score()), str(self._black_player.get_score()),
                                           str(self.current_snapshot_index + 1), str(len(self.snapshots)))

        # print("Board: ", self._board.get_piece_board())
        # print("Coloring: ", self._board.get_coloring_board())

    def bottom_left_button_click(self) -> None:
        self.prev_snapshot()
        self._update_player()
        self._update_board()
        self._update_gui()

    def bottom_right_button_click(self) -> None:
        self.next_snapshot()
        self._update_player()
        self._update_board()
        self._update_gui()


    def top_left_button_click(self) -> None:
        opponent_attacked_fields = set()
        self._opponent_player.update_pieces_attacked_fields(self._current_player)
        for piece in self._opponent_player._pieces:
            for field in piece._attacked_fields:
                opponent_attacked_fields.add(field)

        self._gui_controller.update_board_coloring(None, opponent_attacked_fields,
                                                   None, None)

    def top_right_button_click(self) -> None:
        pass

    def click_on_board(self, row: int, col: int) -> None:

        if not self.is_game_over:
            # A selected piece is clicked -> deselect it
            if self._current_player.is_selected_piece_at(row, col):
                self._current_player.selected_piece = None
                self._update_gui()

            # Own unselected piece is clicked -> select it
            elif self._current_player.has_piece_at(row, col):
                self._current_player.set_selected_piece(row, col)

                self._update_gui()

            # Selected piece can move to the square -> move it
            elif self._current_player.is_possible_move(row, col):
                self.make_move(row, col)

            # Empty square or opponent's piece -> deselect the selected piece
            else:
                self._current_player.selected_piece = None
                self._update_gui()

    def make_move(self, row: int, col: int):
        # If next_snapshots isn't an empty list that means that we see a previous state, so it is invalid to make a move
        # Or if we'd like to permit the change than the next_snapshots has to be deleted. TODO: decide
        if len(self.snapshots) - 1 == self.current_snapshot_index:
            self._make_move(row, col)
            self._current_player.selected_piece = None
            self.next_turn()
        else:
            print("Invalid move. You can't make a move in the past.")
            print("Next snapshots: ", len(self.snapshots))

    def _make_move(self, to_row: int, to_col: int) -> None:
        if self._current_player.selected_piece is None:
            print("Error: No piece is selected.")

        from_row = self._current_player.selected_piece.row
        from_col = self._current_player.selected_piece.col

        # Set is_en_passant field if the pawn moves two squares
        self._current_player.reset_en_passant()
        if isinstance(self._current_player.selected_piece, Pawn):
            if abs(from_row - to_row) == 2:
                self._current_player.selected_piece.is_en_passant = True

        # Check if the move is a promotion
        if self.is_promotion(to_row):
            if isinstance(self._current_player, ComputerPlayer):
                piece_type = PieceType.QUEEN
            else:
                piece_type: PieceType = self._gui_controller.get_type_from_promotion_dialog(self._current_player.color)
            self._current_player.do_promotion(to_row, to_col, piece_type)
            if self._opponent_player.has_piece_at(to_row, to_col):
                self._opponent_player.remove_piece_at(to_row, to_col)

        # Check if the move is a castling
        elif self.is_castling(to_col):
            self._current_player.do_castling(to_row, to_col)

        # Check if the move is an en passant
        elif self.is_en_passant(to_row, to_col):
            self._current_player.do_en_passant(to_row, to_col)
            if self._current_player.color == Color.WHITE:
                self._opponent_player.remove_piece_at(to_row + 1, to_col)
            else:
                self._opponent_player.remove_piece_at(to_row - 1, to_col)

        # Normal move
        else:
            self._current_player.move_piece(to_row, to_col)
            if self._opponent_player is not None and self._opponent_player.has_piece_at(to_row, to_col):
                self._opponent_player.remove_piece_at(to_row, to_col)

        self._current_player.last_move = (from_row, from_col, to_row, to_col)
        self.step_history.add_step(self._current_player.selected_piece.type.name,
                                   self._current_player.selected_piece.color.name,
                                   from_row, from_col, to_row, to_col)

    def is_promotion(self, to_row: int) -> bool:
        return ((to_row == 0) or (to_row == 7)) and self._current_player.selected_piece.type == PieceType.PAWN

    def is_en_passant(self, to_row: int, to_col: int) -> bool:
        selected_piece = self._current_player.selected_piece
        return (selected_piece.type == PieceType.PAWN and
                to_col != selected_piece.col and
                not self._opponent_player.has_piece_at(to_row, to_col))

    def is_castling(self, to_col: int) -> bool:
        selected_piece = self._current_player.selected_piece
        return (selected_piece.type == PieceType.KING and
                abs(selected_piece.col - to_col) > 1)

    def update(self) -> None:
        self._update_player()
        # self._update_board()
        # self._update_gui()

    def _update_player(self) -> None:
        self._current_player.update_pieces_attacked_fields(self._opponent_player)
        self._current_player.update_pieces_possible_fields(self._opponent_player)

    def _update_board(self) -> None:
        self._board.update_piece_board(self._current_player.pieces, self._opponent_player.pieces)
        if self._current_player.selected_piece is not None:
            self._board.update_coloring_board(self._current_player.selected_piece)

    def save_snapshot(self) -> None:
        self.snapshots.append(Snapshot(self._current_player, self._opponent_player))
        self.current_snapshot_index = len(self.snapshots) - 1

    def prev_snapshot(self) -> None:
        if self.current_snapshot_index > 0:
            self.current_snapshot_index -= 1

        snapshot = self.snapshots[self.current_snapshot_index]
        snapshot.load_players(self._current_player, self._opponent_player)

    def next_snapshot(self) -> None:
        if self.current_snapshot_index < len(self.snapshots) - 1:
            self.current_snapshot_index += 1

        snapshot = self.snapshots[self.current_snapshot_index]
        snapshot.load_players(self._current_player, self._opponent_player)
