import functools
import time

import src.model.Board as Board
from src.model.ColorEnum import ColorEnum
from src.model.Player import Player


class DataUpdater:
    def __init__(self):
        self.data = None

    @staticmethod
    def timer_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            # print(f"Starting {func.__name__} at {start_time}")
            result = func(*args, **kwargs)
            end_time = time.time()
            # print(f"Ending {func.__name__} at {end_time}")
            print(f"{func.__name__} ran for {(end_time - start_time):.5f} seconds")
            return result

        return wrapper

    def update(self, current_player: Player, opponent_player: Player, board: Board):

        """
        When the game starts, first the players are initialized with their pieces

        # GameController class: start_game() method ->
        # Player class: init_pieces() method
        ----------------------------------------------
        Players are initialized with the following data:

        - self._pieces: ✔ list is filled with the pieces
        - self._piece_coordinates: ✔ set is filled with the coordinates of the pieces
        - self._selected_piece: x
        - self._last_moved_piece: x
        - self._possible_moves: x
        - self._all_possible_move: x
        - self._protected_fields: x
        - self._special_moves: x
        - self._attacked_fields: x

        # DataUpdater class: update() method -> update_players() method ->
        # Player class -> update_pieces_data() method
        ----------------------------------------------
        Pieces are updated with the following data:

        - possible_fields: ✔
        - protected_fields: ✔
        - attacked_fields: ✔ (it is the same as possible_fields except for the pawns)

        # Player: update_possible_moves_of_selected_piece() method
        ----------------------------------------------
        if not None:
        Selected_piece got updated with the following data:

        - possible_fields: ✔
        - protected_fields: ✔
        - attacked_fields: ✔

        # Player: get_special_moves() method
        ----------------------------------------------
        En passant and castling moves are added to the special_moves list if they are possible.





        """

        self.update_players(current_player, opponent_player, board)
        self.update_board(current_player, opponent_player, board)

    def update_players(self, current_player: Player, opponent_player: Player, board: Board):
        # 0. Update pieces data
        current_player.update_pieces_data()
        opponent_player.update_pieces_data()

        # 1. Update possible moves of selected piece
        current_player.update_possible_moves_of_selected_piece(board)
        opponent_player.update_possible_moves_of_selected_piece(board)

        # 2. Update special moves (castling, en passant) - later maybe promotion
        current_player.get_special_moves(opponent_player.last_moved_piece)
        opponent_player.get_special_moves(current_player.last_moved_piece)

        # 3-4. Update attacked locations
        #      Update protected fields
        current_player.update_protected_and_attacked_fields()
        opponent_player.update_protected_and_attacked_fields()

    def update_board(self, current_player: Player, opponent_player: Player, board: Board):
        # It has the following boards:
        # 1. Piece board -> the positions of the pieces
        # 2. Coloring board -> the coloring of the squares (view)
        # 3. Attack boards -> the attacked fields by the players
        # 4. Protection boards -> the protected fields by the players

        if current_player.color == ColorEnum.WHITE:
            # The boards methods' parameters are the white player's data first, then the black player's data
            board.update_piece_board(current_player.pieces, opponent_player.pieces)
            board.update_attack_boards(current_player.attacked_fields,
                                             opponent_player.attacked_fields)

            board.update_protection_boards(current_player.protected_fields,
                                                 opponent_player.protected_fields)
        else:
            board.update_piece_board(opponent_player.pieces, current_player.pieces)
            board.update_attack_boards(opponent_player.attacked_fields,
                                             current_player.attacked_fields)
            board.update_protection_boards(opponent_player.protected_fields,
                                                 current_player.protected_fields)

        board.update_coloring_board(current_player.selected_piece, current_player.special_moves)

    def get_data(self):
        return self.data