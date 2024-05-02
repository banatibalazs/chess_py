import functools
import time
from src.model.ColorEnum import ColorEnum



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

    # @timer_decorator
    def update(self, current_player, opponent_player, board):
        self.update_players(current_player, opponent_player, board)
        self.update_board(current_player, opponent_player, board)


    def update_players(self, current_player, opponent_player, board):
        """ """
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
                8. self._king: ✔




                # DataUpdater class: update() method -> update_players() method ->
                # Player class -> update_pieces_data() method
                --------------------------------------------------------------------------------
                |# Piece class -> update_piece() method                                        |
                --------------------------------------------------------------------------------
                :parameter: board                                           -> Board class: 1. piece_board (below)

                Pieces are updated with the following data:

                - possible_fields: ✔
                - protected_fields: ✔
                - attacked_fields: ✔ (it is the same as possible_fields except for the pawns)




                # Player class: update_possible_moves_of_selected_piece() method
                --------------------------------------------------------------------------------
                |# Piece class -> update_piece() method                                        |
                --------------------------------------------------------------------------------
                :parameter: board                                           -> Board class: 1. piece_board (below)

                *** This method is redundant, after the update_pieces_data() method,
                the selected piece is already updated. *** #TODO: Remove this method

                if not None:
                Selected_piece got updated with the following data:

                -I. possible_fields: ✔
                -II. protected_fields: ✔
                -III. attacked_fields: ✔ (it is the same as possible_fields except for the pawns)
                
            ************************************** King is an exception: ********************************************* 
                
                #TODO: Instead of this solution, simulate a move and check if the king is attacked.
                - get the possible moves of the king
                - iterate over the possible moves
                - if the king is attacked, remove the move from the possible moves
                - en passant can be ignored, because the king cannot be attacked by it
                the pawn is already attacking the field. Castling is not an option either.
                
                For doing this, the following data is needed:
                - piece_board -> easy to get, deepcopy and change the piece's position ✔
                - opponent's attacked_fields -> we iterate over the possible moves of the pieces using the 
                modified piece_board ✔
                 
                - But where to update it?
                - I need a reference to the opponent. I should do it in the King class.
                - If I had a reference to the opponent in the Player class.
                
                In the King class the possible moves and the attached fields are not the same just like in Pawn.
                I make a new method in the King class which gets the opponent's pieces as a parameter.
                
                And I have to make this simulation not only for the king but for every piece.
                Because it is possible that the king would be attacked if I move away with a piece.
                
                Every piece will have two methods:
                One to determine the possible moves like now.
                And another one to simulate the move and remove the moves which would result in the king being attacked.
                
                
                - after we finished the simulation, we use the original piece board to reset the opponents pieces ✔
                - opponent's protected_fields ----> This is not necessary if we simulate the move.
            **********************************************************************************************************
                It uses not only the piece_board but also the attacked_fields of the opponent player.
                  piece_board = board.get_piece_board()
                  white_attacked_fields = board.get_white_attack_board()      -> Board class: 3-4. attack_board (below) 
                  black_attacked_fields = board.get_black_attack_board()       
                  white_protected_fields = board.get_white_protection_board() -> Board class: 5-6. protection_board (below)
                  black_protected_fields = board.get_black_protection_board()

                -----------------------------------------------------------------------------------------
                |# Player class: get_special_moves() method -> add_en_passant_to_special_moves() method |
                |                                              add_castling_to_special_moves() method   |
                -----------------------------------------------------------------------------------------
                :parameter: opponent_last_moved_piece                       -> Player class: 4. last_moved_piece
                Uses the self._king field to check if the king is moved.    -> Player class: 8. king (above)

                En passant and castling moves are added to the special_moves list if they are possible.
                resets the special_moves set and adds the special moves to it.

                6. special_moves: ✔


                --------------------------------------------------------------------------------
                # Player: update_protected_and_attacked_fields() method                        |
                --------------------------------------------------------------------------------
                Uses the pieces' - possible_fields property                 -> Piece class I. (above)
                                 - attacked_fields property                 -> Piece class III. (above)

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
                8. self._king: ✔

                Pieces are updated with the following data:

                  I. possible_fields: ✔
                 II. protected_fields: ✔
                III. attacked_fields: ✔

                ===============================================================================
                """
        # 0. Update pieces data
        current_player.update_pieces_attacked_fields(opponent_player)
        opponent_player.update_pieces_attacked_fields(current_player)

        current_player.update_pieces_attacked_fields(opponent_player)
        opponent_player.update_pieces_attacked_fields(current_player)

        current_player.update_pieces_protected_fields()
        opponent_player.update_pieces_protected_fields()

        current_player.update_pieces_protected_fields()
        opponent_player.update_pieces_protected_fields()


        current_player.update_pieces_possible_fields(opponent_player)
        opponent_player.update_pieces_possible_fields(current_player)

        current_player.update_pieces_possible_fields(opponent_player)
        opponent_player.update_pieces_possible_fields(current_player)

        # # 1. Update possible moves of selected piece
        # current_player.update_possible_moves_of_selected_piece()
        # opponent_player.update_possible_moves_of_selected_piece()

        # 2. Update special moves (castling, en passant) - later maybe promotion
        current_player.get_special_moves(opponent_player.last_moved_piece)
        opponent_player.get_special_moves(current_player.last_moved_piece)

        # 3-4. Update attacked locations
        #      Update protected fields
        current_player.update_protected_and_attacked_fields()
        opponent_player.update_protected_and_attacked_fields()

    def update_board(self, current_player, opponent_player, board):
        """ """
        """
        Board class:
        1. piece_board: the positions of the pieces - ByteArray8x8
        2. coloring_board: the coloring of the squares (view) - CharArray8x8
        3. white attack board: the attacked fields by the white player - BoolArray8x8
        4. black attack board: the attacked fields by the black player - BoolArray8x8
        5. white protection board: the protected fields by the white player - BoolArray8x8
        6. black protection board: the protected fields by the black player - BoolArray8x8

        -----------------------------------------------------------------------------
        |# DataUpdater class: update() method -> update_board() method ->            |
        |# Board class -> update_piece_board() method                                |
        -----------------------------------------------------------------------------
            1. piece_board: ✔
                - parameters: white_player_pieces, black_player_pieces          -> Player class: 1. pieces

        -----------------------------------------------------------------------------
        |# Board class: update_attack_boards() method                               |
        -----------------------------------------------------------------------------
            3-4. white attack board, black attack board: ✔
                - parameters: attacked_fields, attacked_by_black                -> Player class: 7. attacked_fields

        -----------------------------------------------------------------------------
        |# Board class: update_protection_boards() method                            |
        -----------------------------------------------------------------------------
            5-6. white protection board, black protection board: ✔
                - parameters: protected_fields, protected_by_black              -> Player class: 5. protected_fields

        -----------------------------------------------------------------------------
        |# Board class: update_coloring_board() method                               |
        -----------------------------------------------------------------------------
            2. coloring_board: ✔
                - parameters: selected_piece, special_moves                     -> Player class: 3. selected_piece,
                                                                                                 6. special_moves
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
        
        1. Player class -> init_pieces() method    
        2. Board class  -> update_piece_board() method  - ByteArray8x8
        3. Player class -> update_pieces_data() method -> Piece class -> update_piece() method 
        4. Player class -> update_protected_and_attacked_fields() method
        5. Board class  -> update_attack_boards() method - BoolArray8x8
        6. Board class  -> update_protection_boards() method - BoolArray8x8
        7. Player class -> get_special_moves() method -> add_en_passant_to_special_moves() method
                                                      -> add_castling_to_special_moves() method  
        *8. Select the piece and update the coloring board
            - set selected_piece
            - set special_moves
            - set coloring_board
        
        *9. If move is made, what changes?
            - update the coordinates of the piece
            - update the piece_board
            - update the possible fields of every piece
            - update the attack boards
            - update the protection boards
            - update the coloring board
        
        *10. If special move is made, what changes?
            - update the piece_board
            - update the attack boards
            - update the protection boards
            - update the coloring board
        
        """



    def get_data(self):
        return self.data