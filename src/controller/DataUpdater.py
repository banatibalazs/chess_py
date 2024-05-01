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
        self.update_players(current_player, opponent_player, board)
        self.update_board(current_player, opponent_player, board)

    def update_players(self, current_player: Player, opponent_player: Player, board: Board):
        """
                When the game starts, first the players are initialized with their pieces



                # GameController class: start_game() method ->
                --------------------------------------------------------------------------------
                |# Player class: init_pieces() method                                          |
                --------------------------------------------------------------------------------
                Players are initialized with the following data:

                1. self._pieces: ✔ list is filled with the pieces
                2. self._piece_coordinates: ✔ set is filled with the coordinates of the pieces
                3. self._selected_piece: x
                4. self._last_moved_piece: x
                5. self._protected_fields: x
                6. self._special_moves: x
                7. self._attacked_fields: x




                # DataUpdater class: update() method -> update_players() method ->
                # Player class -> update_pieces_data() method
                --------------------------------------------------------------------------------
                |# Piece class -> update_piece() method                                        |
                --------------------------------------------------------------------------------
                :parameter: board -> Board class: 1. piece_board (below)

                Pieces are updated with the following data:

                - possible_fields: ✔
                - protected_fields: ✔
                - attacked_fields: ✔ (it is the same as possible_fields except for the pawns)




                # Player: update_possible_moves_of_selected_piece() method
                --------------------------------------------------------------------------------
                |# Piece class -> update_piece() method                                        |
                --------------------------------------------------------------------------------
                :parameter: board -> Board class: 1. piece_board (below)

                *** This method is redundant, after the update_pieces_data() method,
                the selected piece is already updated. *** #TODO: Remove this method

                if not None:
                Selected_piece got updated with the following data:

                - possible_fields: ✔
                - protected_fields: ✔
                - attacked_fields: ✔


                --------------------------------------------------------------------------------
                # Player: get_special_moves() method -> add_en_passant_to_special_moves() method
                                                        add_castling_to_special_moves() method
                --------------------------------------------------------------------------------
                :parameter: last_moved_piece -> Piece class: 1. last_moved_piece

                En passant and castling moves are added to the special_moves list if they are possible.
                resets the special_moves set and adds the special moves to it.

                6. special_moves: ✔


                --------------------------------------------------------------------------------
                # Player: update_protected_and_attacked_fields() method                        |
                --------------------------------------------------------------------------------
                Resets the protected_fields and attacked_fields sets and adds the new data to them.

                5. protected_fields: ✔
                7. attacked_fields: ✔

                ===============================================================================
                Summary:
                ==============================================================================
                Players are updated with the following data:

                1. self._pieces: ✔
                2. self._piece_coordinates: ✔
                3. self._selected_piece: x
                4. self._last_moved_piece: x
                5. self._protected_fields: ✔
                6. self._special_moves: ✔
                7. self._attacked_fields: ✔

                Pieces are updated with the following data:

                - possible_fields: ✔
                - protected_fields: ✔
                - attacked_fields: ✔

                ===============================================================================
                """
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

        """
        Board class:
        1. piece_board: the positions of the pieces - ByteArray8x8
        2. coloring_board: the coloring of the squares (view) - CharArray8x8
        3. white attack board: the attacked fields by the white player - BoolArray8x8
        4. black attack board: the attacked fields by the black player - BoolArray8x8
        5. white protection board: the protected fields by the white player - BoolArray8x8
        6. black protection board: the protected fields by the black player - BoolArray8x8


        # DataUpdater class: update() method -> update_board() method ->
        # Board class -> update_piece_board() method
        ----------------------------------------------
        1. piece_board: ✔
            - parameters: white_player_pieces, black_player_pieces - Player class: 1. pieces

        # Board class: update_attack_boards() method
        ----------------------------------------------
        3-4. white attack board, black attack board: ✔
            - parameters: attacked_fields, attacked_by_black - Player class: 7. attacked_fields


        # Board class: update_protection_boards() method
        ----------------------------------------------
        5-6. white protection board, black protection board: ✔
            - parameters: protected_fields, protected_by_black - Player class: 5. protected_fields


        # Board class: update_coloring_board() method
        ----------------------------------------------
        2. coloring_board: ✔
            - parameters: selected_piece, special_moves - Player class: 3. selected_piece, 6. special_moves
            ** The method only uses the coordinates of the selected piece and its possible moves. **

        ==============================================
        Summary:
        ==============================================
        Board is updated with the following data:

        1. piece_board: ✔
        2. coloring_board: ✔
        3. white attack board: ✔
        4. black attack board: ✔
        5. white protection board: ✔
        6. black protection board: ✔

        ==============================================


        """

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

    """
    A better way to update the data:
    
    1. Initialize the Players with pieces
    2. Update the piece_board with the current piece positions
    3. Update the 
    
    """



    def get_data(self):
        return self.data