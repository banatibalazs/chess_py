import time as tm
import os
import psutil
from typing import Optional

from src.controller.game_saver import GameSaver
from src.controller.gui_controller import GuiController
from src.controller.timer_thread import TimerThread
from src.model.board import Board
from src.model.enums.color import Color
from src.model.players.alpha_beta_player import AlphaBeta
from src.model.players.greedy_player import GreedyPlayer
from src.model.players.random_player import RandomPlayer
from src.model.enums.game_result import GameResult
from src.model.pieces.pawn import Pawn
from src.model.enums.piece_type import PieceType
from src.model.players.player import Player
from src.model.enums.player_type import PlayerType
from src.view.chess_gui import ChessGui


class Game:
    def __init__(self, title: str, white_player_name: str, white_player_type: PlayerType, black_player_name: str,
                 black_player_type: PlayerType, _time: Optional[int], pov: Color) -> None:

        self.gui: ChessGui = ChessGui(title, pov, white_player_name, black_player_name, _time,
                                      self.click_on_board, self.bottom_right_button_click,
                                      self.bottom_left_button_click)
        if _time is None:
            self.timer = None
        else:
            self.timer = TimerThread(self)

        self._gui_controller: GuiController = GuiController(self.gui)

        self._board: Board = Board()
        if white_player_type == PlayerType.HUMAN:
            self._white_player: Player = Player(white_player_name, Color.WHITE, self._board, _time)
        elif white_player_type == PlayerType.RANDOM:
            self._white_player: Player = RandomPlayer(white_player_name, Color.WHITE, self._board, _time)
        elif white_player_type == PlayerType.GREEDY:
            self._white_player: Player = GreedyPlayer(white_player_name, Color.WHITE, self._board, _time)
        elif white_player_type == PlayerType.MINIMAX:
            self._white_player: Player = AlphaBeta(white_player_name, Color.WHITE, self._board, _time)
        else:
            self._white_player: Player = Player(white_player_name, Color.WHITE, self._board, _time)

        if black_player_type == PlayerType.HUMAN:
            self._black_player: Player = Player(black_player_name, Color.BLACK, self._board, _time)
        elif black_player_type == PlayerType.RANDOM:
            self._black_player: Player = RandomPlayer(black_player_name, Color.BLACK, self._board, _time)
        elif black_player_type == PlayerType.GREEDY:
            self._black_player: Player = GreedyPlayer(black_player_name, Color.BLACK, self._board, _time)
        elif black_player_type == PlayerType.MINIMAX:
            self._black_player: Player = AlphaBeta(black_player_name, Color.BLACK, self._board, _time)
        else:
            self._black_player: Player = Player(black_player_name, Color.BLACK, self._board, _time)
        self._current_player: Player = self._white_player
        self._opponent_player: Player = self._black_player

        self.is_game_over: bool = False

        self.game_saver: GameSaver = GameSaver()

        self.start_time = tm.time()
        self.start_game()

    def __del__(self):
        if self.timer is not None:
            self.timer.stop()
        print("Game destroyed.")

    def start_game(self) -> None:
        self._white_player.init_pieces()
        self._black_player.init_pieces()

        if self.timer is not None:
            self.timer.start()

        self.game_saver.save_game(self._current_player, self._opponent_player)
        self._update_player()
        self._update_board()
        self._update_gui()

        if isinstance(self._current_player, RandomPlayer) or isinstance(self._current_player, GreedyPlayer):
            move = self._current_player.choose_move(self._opponent_player)
            self.make_move(move[0], move[1])

    def next_turn(self) -> None:
        self._current_player, self._opponent_player = self._opponent_player, self._current_player
        self.game_saver.save_game(self._current_player, self._opponent_player)

        if not isinstance(self._current_player, RandomPlayer) or not isinstance(self._opponent_player, RandomPlayer):
            self._update_player()
            self._update_board()
            self._update_gui()
        else:
            self._update_player()

        print(str(self.game_saver.total_states()))
        self.check_if_game_over()

        if not self.is_game_over and (isinstance(self._current_player, RandomPlayer) or\
                isinstance(self._current_player, GreedyPlayer) or\
                isinstance(self._current_player, AlphaBeta)):
            move = self._current_player.choose_move(self._opponent_player)
            if move is not None:
                self.make_move(move[0], move[1])
            else:
                print("No possible moves.")
                self.end_game(GameResult.DRAW_BY_STALEMATE)

    def check_if_game_over(self) -> None:
        if len(self._current_player.pieces) == 1 and len(self._opponent_player.pieces) == 1:
            # print("Draw: Only two kings left.")
            self.end_game(GameResult.DRAW_BY_INSUFFICIENT_MATERIAL)

        if not self._current_player.can_move():
            if self._current_player.king.is_in_check:
                # print(f"Checkmate: {self._current_player.color.name} {self._current_player.name} can't move.")
                self.end_game(GameResult.WHITE_WON_BY_CHECKMATE if self._current_player.color == Color.BLACK else
                              GameResult.BLACK_WON_BY_CHECKMATE)
            else:
                print(f"{self._current_player.name} can't move.")
                self.end_game(GameResult.DRAW_BY_STALEMATE)

        if self.game_saver.is_threefold_repetition:
            print("Draw: Threefold repetition.")
            self.end_game(GameResult.DRAW_BY_THREEFOLD_REPETITION)

    def end_game(self, game_result: GameResult) -> None:
        self.is_game_over = True
        if self.timer is not None:
            self.timer.stop()
        self._update_board()
        self._update_gui()
        try:
            print(f"Memory usage: {self.get_memory_usage()} MB")
            print("Game lasted: ", tm.time() - self.start_time, " seconds.")
            print("That is ", (self.game_saver.total_states() + 1) / (tm.time() - self.start_time), " steps per second.")
            print("One step takes ", 1 / ((self.game_saver.total_states() + 1)/ (tm.time() - self.start_time)), " seconds.")
        except Exception as e:
            print(e)

        self._gui_controller.end_game_dialog(game_result)

    def get_memory_usage(self):
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        return mem_info.rss / 1024 / 1024  # return memory usage in MB

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

        if self._current_player.color == Color.WHITE:
            white_score = str(self._current_player.get_score())
            black_score = str(self._opponent_player.get_score())
        else:
            white_score = str(self._opponent_player.get_score())
            black_score = str(self._current_player.get_score())

        self._gui_controller.update_labels(white_score, black_score,
                                           str(self.game_saver.current_state_index()), str(self.game_saver.total_states()))

        # print("Board: ", self._board.get_piece_board())
        # print("Coloring: ", self._board.get_coloring_board())

    def bottom_left_button_click(self) -> None:
        self.game_saver.load_previous_state(self._current_player, self._opponent_player)
        self._update_player()
        self._update_board()
        self._update_gui()

    def bottom_right_button_click(self) -> None:
        self.game_saver.load_next_state(self._current_player, self._opponent_player)
        self._update_player()
        self._update_board()
        self._update_gui()


    def top_left_button_click(self) -> None:
        opponent_attacked_fields = set()

        self._opponent_player.update_pieces_attacked_fields(self._current_player.piece_coordinates)
        for piece in self._opponent_player._pieces:
            for field in piece._attacked_fields:
                opponent_attacked_fields.add(field)

        self._gui_controller.update_board_coloring(None, opponent_attacked_fields,
                                                   None, None)

    def top_right_button_click(self) -> None:
        pass

    def click_on_board(self, row: int, col: int) -> None:
        print(f"Clicked on: {row}, {col}")
        if not self.is_game_over:
            # A selected piece is clicked -> deselect it
            if self._current_player.is_selected_piece_at(row, col):
                print("Deselecting the piece.")
                self._current_player.selected_piece = None
                self._update_gui()

            # Own unselected piece is clicked -> select it
            elif self._current_player.has_piece_at(row, col):
                self._current_player.set_selected_piece(row, col)
                print("Selecting the piece.")
                self._update_gui()

            # Selected piece can move to the square -> move it
            elif self._current_player.is_possible_move(row, col):
                self.make_move(row, col)
                print("Making a move.")

            # Empty square or opponent's piece -> deselect the selected piece
            else:
                print("Invalid square.")
                self._current_player.selected_piece = None
                self._update_gui()

    def make_move(self, row: int, col: int):
        # If next_snapshots isn't an empty list that means that we see a previous state, so it is invalid to make a move
        # Or if we'd like to permit the change than the next_snapshots has to be deleted. TODO: decide
        if self.game_saver.is_current_state():
            self._make_move(row, col)
            self._current_player.selected_piece = None
            self.next_turn()
        else:
            print("Invalid move. You can't make a move in the past.")

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
                # print("En passant is possible.")

        # Check if the move is a promotion
        if self.is_promotion(to_row):
            if isinstance(self._current_player, RandomPlayer) or isinstance(self._current_player, GreedyPlayer):
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
        # self.step_history.add_step(self._current_player.selected_piece.type.name,
        #                            self._current_player.selected_piece.color.name,
        #                            from_row, from_col, to_row, to_col)

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
        self._current_player.update_pieces_attacked_fields(self._opponent_player.piece_coordinates)
        self._opponent_player.update_pieces_attacked_fields(self._current_player.piece_coordinates)
        self._current_player.update_pieces_possible_fields(self._opponent_player)

    def _update_board(self) -> None:
        self._board.update_piece_board(self._current_player.pieces, self._opponent_player.pieces)
        if self._current_player.selected_piece is not None:
            self._board.update_coloring_board(self._current_player.selected_piece)

    def nothing(self, row, col) -> None:
        print("Row, col: " ,row, col)

