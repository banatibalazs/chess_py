

class GameController:

    def __init__(self, white_player_name, black_player_name, view_controller):
        self._white_player_name = white_player_name
        self._black_player_name = black_player_name
        self._is_white_turn = True
        self._view_controller = view_controller
        self._piece_positions_board = []
        self.initialize_board()
        # History is a stack of tuples (board, is_white_turn)
        self._boardHistory = []

    def initialize_board(self):
        self._piece_positions_board = [[-2,-3,-4,-5,-6,-4,-3,-2],
                                       [-1,-1,-1,-1,-1,-1,-1,-1],
                                       [ 0, 0, 0, 0, 0, 0, 0, 0],
                                       [ 0, 0, 0, 0 ,0 ,0 ,0 ,0],
                                       [ 0, 0, 0, 0, 0, 0, 0, 0],
                                       [ 0, 0, 0, 0, 0, 0, 0, 0],
                                       [ 1, 1, 1, 1, 1, 1, 1, 1],
                                       [ 2, 3, 4, 5, 6, 4, 3, 2]]

        self._view_controller.update_board(self._piece_positions_board)

    def click_on_square(self, x, y):

         if self._piece_positions_board[x][y] == 0:
             print("Empty square")
         elif self._is_white_turn and self._piece_positions_board[x][y] < 0:
             print("Black piece selected")
         else:
             print("White piece selected")

         print( "White Turn!" if self._is_white_turn else "Black Turn!")



    def step(self):
        pass

    def save_game(self):
        pass

    def load_game(self):
        pass