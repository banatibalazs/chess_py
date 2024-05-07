from typing import List

from src.controller.DataUpdater import DataUpdater
# from src.controller.TimerThread import TimerThread
from src.model.Bishop import Bishop
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.King import King
from src.model.Knight import Knight
from src.model.Pawn import Pawn
from src.model.PieceTypeEnum import PieceTypeEnum
from src.model.Player import Player
from src.model.Queen import Queen
from src.model.Rook import Rook


class GameController:

    def __init__(self, white_player_name: str, black_player_name: str, view_controller):
        self._board: Board = Board()

        self._white_player: Player = Player(white_player_name, ColorEnum.WHITE, self._board)
        self._black_player: Player = Player(black_player_name, ColorEnum.BLACK, self._board)
        self._current_player: Player = self._white_player
        self._opponent_player: Player = self._black_player

        self.data_updater = DataUpdater()
        self.is_white_turn: bool = True
        self._view_controller = view_controller

        # self.black_timer = TimerThread(300, black_player_name, self)  # 5 minutes timer
        # self.white_timer = TimerThread(300, white_player_name, self)  # 5 minutes timer
        # self._board_history_prev: List[Board] = []
        # self._board_history_fwd: List[Board] = []

        self.start_game()

    def start_game(self):
        self._white_player.init_pieces()
        self._black_player.init_pieces()

        self.data_updater.update(self._white_player, self._black_player, self._board)
        self.update_view()

    def next_turn(self):
        self.data_updater.update(self._current_player, self._opponent_player, self._board)
        self.update_view()
        self.is_white_turn = not self.is_white_turn
        self._current_player, self._opponent_player = self._opponent_player, self._current_player

    def update_view(self) -> None:
        self.data_updater.update(self._current_player, self._opponent_player, self._board)

        self._view_controller.update_pieces_on_board(self._board.get_piece_board())
        self._view_controller.update_board_coloring(self._board.get_coloring_board())
        self._view_controller.update_labels(str(self._white_player.get_score()), str(self._black_player.get_score()))

        # print("Board: ", self._board.get_piece_board())
        # print("Coloring: ", self._board.get_coloring_board())
        # print("White attack: ", self._board.get_white_attack_board())
        # print("Black attack: ", self._board.get_black_attack_board())

    def click_on_white_button(self) -> None:
        self._view_controller.show_white_attack_board(self._board.get_white_attack_board())

    def click_on_black_button(self) -> None:
        self._view_controller.show_black_attack_board(self._board.get_black_attack_board())

    def click_on_white_protection_button(self) -> None:
        self._view_controller.show_protection_board(self._board.get_white_protection_board())

    def click_on_black_protection_button(self) -> None:
        self._view_controller.show_protection_board(self._board.get_black_protection_board())

    def click_on_board(self, row: int, col: int) -> None:

        # print("Clicked on board at: ", row, col)
        # print("Piece: ", self._board.get_piece_board()[row][col])

        # A selected piece is clicked -> deselect it
        if self._current_player.is_selected_piece_at(row, col):
            # print("Deselecting piece")
            self._current_player.selected_piece = None

        # Own unselected piece is clicked -> select it
        elif self._current_player.has_piece_at(row, col):
            # print("Selecting piece")
            self._current_player.set_selected_piece(row, col)

        # Selected piece can move to the square -> move it
        elif self._current_player.is_possible_move(row, col):
            # print("Making move")
            self.make_move(row, col)

        # Empty square or opponent's piece -> deselect the selected piece
        else:
            # print("Empty.")
            self._current_player.selected_piece = None

        self.update_view()

    def make_move(self, row, col):
        self._make_move(row, col)
        self._current_player.selected_piece = None
        self.next_turn()

    def _make_move(self, to_row: int, to_col: int) -> None:
        if self._current_player.selected_piece is None:
            print("Eror: No piece is selected.")

        # Set en passant field if the pawn moves two squares
        self._current_player.reset_en_passant()
        if isinstance(self._current_player.selected_piece, Pawn):
            if abs(self._current_player.selected_piece.row - to_row) == 2:
                print("En passant variable is set.")
                self._current_player.selected_piece.is_en_passant = True

        if self.is_promotion(to_row):
            self.do_promotion(to_row, to_col, PieceTypeEnum.QUEEN)

        elif (to_row, to_col) in self._current_player.special_moves:
            if isinstance(self._current_player.selected_piece, King):
                self.do_castling(to_row, to_col)
            if isinstance(self._current_player.selected_piece, Pawn):
                self.do_en_passant(to_row, to_col, self._opponent_player)

        if self._opponent_player is not None and self._opponent_player.has_piece_at(to_row, to_col):
            self._opponent_player.remove_piece_at(to_row, to_col)

        self._current_player.selected_piece.coordinates = (to_row, to_col)
        self._current_player.selected_piece.is_moved = True
        self._current_player._last_moved_piece = self._current_player.selected_piece

    def do_castling(self, row: int, col: int):
        print("Castling")
        if col == 2:
            rook = self._current_player.get_piece_at(row=row, col=0)
            if rook is not None:
                rook.coordinates = (row, 3)
                rook.set_moved = True
        elif col == 6:
            rook = self._current_player.get_piece_at(row, 7)
            if rook is not None:
                rook.coordinates = (row, 5)
                rook.set_moved = True

        king = self._current_player.get_king()
        if king is not None:
            king.coordinates = (row, col)
            king.set_moved = True
        self._current_player._last_moved_piece = king
        self._current_player.reset_en_passant()

    def do_en_passant(self, to_row, to_col, opponent):
        if self._current_player.color == ColorEnum.WHITE:
            opponent.remove_piece_at(to_row + 1, to_col)
        else:
            opponent.remove_piece_at(to_row - 1, to_col)
        self._current_player.selected_piece.coordinates = (to_row, to_col)
        self._current_player.reset_en_passant()

    def is_promotion(self, to_row):
        return ((to_row == 0) or (to_row == 7)) and isinstance(self._current_player.selected_piece, Pawn)

    def do_promotion(self, to_row: int, to_col: int, piece_type: PieceTypeEnum) -> None:
        print("Promoting pawn")
        from_row = self._current_player.selected_piece.row
        from_col = self._current_player.selected_piece.col

        self._current_player.remove_piece_at(from_row, from_col)
        if piece_type == PieceTypeEnum.QUEEN:
            new_piece = Queen(self._current_player.color, to_row, to_col)
        elif piece_type == PieceTypeEnum.ROOK:
            new_piece = Rook(self._current_player.color, to_row, to_col)
        elif piece_type == PieceTypeEnum.BISHOP:
            new_piece = Bishop(self._current_player.color, to_row, to_col)
        elif piece_type == PieceTypeEnum.KNIGHT:
            new_piece = Knight(self._current_player.color, to_row, to_col)
        else:
            raise ValueError("Invalid piece type.")
        self._current_player.pieces.append(new_piece)
        self._current_player.last_moved_piece = new_piece
        self._current_player.reset_en_passant()


    def save_game(self):
        # current_data = [self._board._piece_board, self._board._current_player.get_color(),
        #                 self._board._current_player_name, self._board._opponent_player_name]
        # self._board_history_prev.append()
        pass

    def load_game_prev(self):
        # self._board_history_fwd.append(self._board)
        # self._board = self._board_history_prev.pop()
        pass

    def load_game_fwd(self):
        # current_data = [self._board._current_player, self._board._opponent_player]
        # self._board_history_prev.append()
        # self._board.load_players(self._board_history_fwd.pop())
        pass

