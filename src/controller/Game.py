from typing import List

from src.controller.Snapshot import Snapshot
from src.controller.GuiController import GuiController
from src.controller.StepHistory import StepHistory
from src.model.Bishop import Bishop
from src.model.Board import Board
from src.model.Color import Color
from src.model.Knight import Knight
from src.model.Pawn import Pawn
from src.model.PieceType import PieceType
from src.model.Player import Player
from src.model.Queen import Queen
from src.model.Rook import Rook
from src.view.ChessGui import ChessGui


class Game:
    def __init__(self, title: str, white_player_name: str, black_player_name: str) -> None:

        self.gui: ChessGui = ChessGui(title, white_player_name, black_player_name,
                            self.click_on_board, self.top_left_button_click,
                            self.top_right_button_click, self.bottom_right_button_click,
                            self.bottom_left_button_click)
        self._gui_controller: GuiController = GuiController(self.gui)

        self._board: Board = Board()
        self._white_player: Player = Player(white_player_name, Color.WHITE, self._board)
        self._black_player: Player = Player(black_player_name, Color.BLACK, self._board)
        self._current_player: Player = self._white_player
        self._opponent_player: Player = self._black_player

        self.is_white_turn: bool = True

        self.step_history: StepHistory = StepHistory()
        self.snapshots: List[Snapshot] = []
        self.current_snapshot_index = 0

        self.start_game()

    def start_game(self) -> None:
        self._white_player.init_pieces()
        self._black_player.init_pieces()

        self.save_snapshot()
        self.update()

    def next_turn(self) -> None:
        self.update()
        self.is_white_turn = not self.is_white_turn
        self._current_player, self._opponent_player = self._opponent_player, self._current_player
        self.save_snapshot()
        print(self.step_history.get_steps())

    def _update_gui(self) -> None:
        self._gui_controller.update_pieces_on_board(self._board.get_piece_board())

        coordinates = None
        possible_fields = None

        if self._current_player.selected_piece is not None:
            coordinates = self._current_player.selected_piece.coordinates
            possible_fields = self._current_player.selected_piece.possible_fields

        last_move = self._opponent_player.last_move

        self._gui_controller.update_board_coloring(coordinates, possible_fields, last_move)
        self._gui_controller.update_labels(str(self._white_player.get_score()), str(self._black_player.get_score()),
                                           str(self.current_snapshot_index + 1), str(len(self.snapshots)))

        # print("Board: ", self._board.get_piece_board())
        # print("Coloring: ", self._board.get_coloring_board())

    def bottom_left_button_click(self) -> None:
        self.prev_snapshot()
        self.update()

    def bottom_right_button_click(self) -> None:
        self.next_snapshot()
        self.update()

    def top_left_button_click(self) -> None:
        self._gui_controller.show_white_attack_board(self._board.get_white_attack_board())

    def top_right_button_click(self) -> None:
        self._gui_controller.show_black_attack_board(self._board.get_black_attack_board())

    def click_on_board(self, row: int, col: int) -> None:

        # A selected piece is clicked -> deselect it
        if self._current_player.is_selected_piece_at(row, col):
            self._current_player.selected_piece = None

        # Own unselected piece is clicked -> select it
        elif self._current_player.has_piece_at(row, col):
            self._current_player.set_selected_piece(row, col)

        # Selected piece can move to the square -> move it
        elif self._current_player.is_possible_move(row, col):
            self.make_move(row, col)

        # Empty square or opponent's piece -> deselect the selected piece
        else:
            self._current_player.selected_piece = None

        self.update()

    def make_move(self, row: int, col: int):
        # If next_snapshots isn't an empty list that means that we see a previous state, so it is invalid to make a move
        # Or if we'd like to permit the change than the next_snapshots has to be deleted. TODO
        if len(self.snapshots) - 1 == self.current_snapshot_index:
            self._make_move(row, col)
            self._current_player.selected_piece = None
            self.next_turn()
        else:
            print("Invalid move. You can't make a move in the past.")
            print("Next snapshots: ", len(self.snapshots))

    def _make_move(self, to_row: int, to_col: int) -> None:
        if self._current_player.selected_piece is None:
            print("Eror: No piece is selected.")

        from_row = self._current_player.selected_piece.row
        from_col = self._current_player.selected_piece.col

        # Set en passant field if the pawn moves two squares
        self._current_player.reset_en_passant()
        if isinstance(self._current_player.selected_piece, Pawn):
            if abs(self._current_player.selected_piece.row - to_row) == 2:
                self._current_player.selected_piece.is_en_passant = True

        # Check if the move is a promotion
        if self.is_promotion(to_row):
            self.do_promotion(to_row, to_col, PieceType.QUEEN)

        # Check if the move is a castling
        if self.is_castling(to_col):
            self.do_castling(to_row, to_col)

        # Check if the move is an en passant
        if self.is_en_passant(to_row, to_col):
            self.do_en_passant(to_row, to_col, self._opponent_player)

        if self._opponent_player is not None and self._opponent_player.has_piece_at(to_row, to_col):
            self._opponent_player.remove_piece_at(to_row, to_col)

        self._current_player.move_piece(to_row, to_col)

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

    def do_castling(self, row: int, col: int) -> None:
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

        king = self._current_player.king
        if king is not None:
            king.coordinates = (row, col)
            king.set_moved = True
        self._current_player._last_moved_piece = king
        self._current_player.reset_en_passant()

    def do_en_passant(self, to_row: int, to_col: int, opponent: Player) -> None:
        print("En passant")
        if self._current_player.color == Color.WHITE:
            opponent.remove_piece_at(to_row + 1, to_col)
        else:
            opponent.remove_piece_at(to_row - 1, to_col)
        self._current_player.selected_piece.coordinates = (to_row, to_col)
        self._current_player.reset_en_passant()

    def do_promotion(self, to_row: int, to_col: int, piece_type: PieceType) -> None:
        print("Promoting pawn")
        from_row = self._current_player.selected_piece.row
        from_col = self._current_player.selected_piece.col

        self._current_player.remove_piece_at(from_row, from_col)
        if piece_type == PieceType.QUEEN:
            new_piece = Queen(self._current_player.color, to_row, to_col)
        elif piece_type == PieceType.ROOK:
            new_piece = Rook(self._current_player.color, to_row, to_col)
        elif piece_type == PieceType.BISHOP:
            new_piece = Bishop(self._current_player.color, to_row, to_col)
        elif piece_type == PieceType.KNIGHT:
            new_piece = Knight(self._current_player.color, to_row, to_col)
        else:
            raise ValueError("Invalid piece type.")
        self._current_player.pieces.append(new_piece)
        self._current_player.last_moved_piece = new_piece
        self._current_player.reset_en_passant()

    def update(self) -> None:
        self._update_players(self._current_player, self._opponent_player)
        self._update_board(self._current_player, self._opponent_player, self._board)
        self._update_gui()

    def _update_players(self, current_player: Player, opponent_player: Player) -> None:
        current_player.update_pieces_attacked_fields(opponent_player)
        opponent_player.update_pieces_attacked_fields(current_player)

    def _update_board(self, current_player: Player, opponent_player: Player, board: Board) -> None:

        board.update_piece_board(current_player, opponent_player)
        board.update_attack_boards(current_player, opponent_player)

        if current_player.selected_piece is not None:
            current_player.selected_piece.update_possible_fields(current_player, opponent_player)
        board.update_coloring_board(current_player.selected_piece)

    def save_snapshot(self) -> None:
        self.snapshots.append(Snapshot(self._current_player, self._opponent_player))
        self.current_snapshot_index = len(self.snapshots) - 1
        print("Snapshot saved.", len(self.snapshots) - 1)

    def prev_snapshot(self) -> None:
        if self.current_snapshot_index > 0:
            self.current_snapshot_index -= 1

        snapshot = self.snapshots[self.current_snapshot_index]
        print(f"Loading snapshot {self.current_snapshot_index} / {len(self.snapshots) - 1}")
        snapshot.load_players(self._current_player, self._opponent_player)

    def next_snapshot(self) -> None:
        if self.current_snapshot_index < len(self.snapshots) - 1:
            self.current_snapshot_index += 1

        snapshot = self.snapshots[self.current_snapshot_index]
        print(f"Loading snapshot {self.current_snapshot_index} / {len(self.snapshots) - 1}")
        snapshot.load_players(self._current_player, self._opponent_player)

