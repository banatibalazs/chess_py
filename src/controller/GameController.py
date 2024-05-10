from src.controller.CustomTypesForTypeHinting import ByteArray8x8
from src.controller.GameSnapshot import GameSnapshot
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

        self.is_white_turn: bool = True
        self._view_controller = view_controller

        self.game_history_prev = []
        self.game_history_fwd = []

        self._snapshots = []

        self.start_game()

    def start_game(self):
        self._white_player.init_pieces()
        self._black_player.init_pieces()

        self.update(self._white_player, self._black_player, self._board)
        self.update_view()

    def next_turn(self):
        self.update(self._current_player, self._opponent_player, self._board)
        self.update_view()
        self.is_white_turn = not self.is_white_turn
        self._current_player, self._opponent_player = self._opponent_player, self._current_player

    def update_view(self) -> None:
        self.update(self._current_player, self._opponent_player, self._board)

        self._view_controller.update_pieces_on_board(self._board.get_piece_board())
        self._view_controller.update_board_coloring(self._board.get_coloring_board())
        self._view_controller.update_labels(str(self._white_player.get_score()), str(self._black_player.get_score()))

        self.save_board(self._board.get_piece_board(), self.is_white_turn)
        # print("Board: ", self._board.get_piece_board())
        # print("Coloring: ", self._board.get_coloring_board())

    def bottom_right_button_click(self) -> None:
        self._view_controller.show_white_attack_board(self._board.get_white_attack_board())

    def top_right_button_click(self) -> None:
        self._view_controller.show_black_attack_board(self._board.get_black_attack_board())

    def bottom_left_button_click(self) -> None:
        pass

    def top_left_button_click(self) -> None:
        pass

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
                self._current_player.selected_piece.is_en_passant = True

        # Check if the move is a promotion
        if self.is_promotion(to_row):
            self.do_promotion(to_row, to_col, PieceTypeEnum.QUEEN)

        # Check if the move is a castling
        if self.is_castling(to_col):
            self.do_castling(to_row, to_col)

        # Check if the move is an en passant
        if self.is_en_passant(to_row, to_col):
            self.do_en_passant(to_row, to_col, self._opponent_player)

        if self._opponent_player is not None and self._opponent_player.has_piece_at(to_row, to_col):
            self._opponent_player.remove_piece_at(to_row, to_col)

        self._current_player.selected_piece.coordinates = (to_row, to_col)
        self._current_player.selected_piece.is_moved = True
        self._current_player._last_moved_piece = self._current_player.selected_piece
        self._current_player.selected_piece.update_attacked_fields(self._current_player, self._opponent_player)

    def is_promotion(self, to_row):
        return ((to_row == 0) or (to_row == 7)) and self._current_player.selected_piece.type == PieceTypeEnum.PAWN

    def is_en_passant(self, to_row, to_col):
        selected_piece = self._current_player.selected_piece
        return (selected_piece.type == PieceTypeEnum.PAWN and
                to_col != selected_piece.col and
                not self._opponent_player.has_piece_at(to_row, to_col))

    def is_castling(self, to_col):
        selected_piece = self._current_player.selected_piece
        return (selected_piece.type == PieceTypeEnum.KING and
                abs(selected_piece.col - to_col) > 1)

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

        king = self._current_player.king
        if king is not None:
            king.coordinates = (row, col)
            king.set_moved = True
        self._current_player._last_moved_piece = king
        self._current_player.reset_en_passant()

    def do_en_passant(self, to_row, to_col, opponent):
        print("En passant")
        if self._current_player.color == ColorEnum.WHITE:
            opponent.remove_piece_at(to_row + 1, to_col)
        else:
            opponent.remove_piece_at(to_row - 1, to_col)
        self._current_player.selected_piece.coordinates = (to_row, to_col)
        self._current_player.reset_en_passant()

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

    def update(self, current_player, opponent_player, board):
        self._update_players(current_player, opponent_player)
        self._update_board(current_player, opponent_player, board)

    def _update_players(self, current_player, opponent_player):
        current_player.update_pieces_attacked_fields(opponent_player)
        opponent_player.update_pieces_attacked_fields(current_player)

    def _update_board(self, current_player, opponent_player, board):

        board.update_piece_board(current_player, opponent_player)
        board.update_attack_boards(current_player, opponent_player)
        # board.update_possible_moves_boards(current_player, opponent_player)

        if current_player.selected_piece is not None:
            current_player.selected_piece.update_possible_fields(current_player, opponent_player)
        board.update_coloring_board(current_player.selected_piece)

    def save_game(self):
        pass

    def load_game_prev(self):
        pass

    def load_game_fwd(self):
        pass

    def save_snapshot(self):
        self._snapshots.append(GameSnapshot(self._current_player, self._opponent_player))

    def load_snapshot(self):
        snapshot = self._snapshots.pop()
        # self._current_player = Pla


    def save_board(self, piece_board: ByteArray8x8, is_white_turn: bool):
        pass

