import numpy as np


class PieceLogics:
    def __init__(self):
        pass

    def get_attacked_fields(self, piece_code: np.byte):
        if piece_code == np.byte(1):
            return self.pawn_logic
        elif piece_code == np.byte(2):
            return self.rook_logic
        elif piece_code == np.byte(3):
            return self.knight_logic
        elif piece_code == np.byte(4):
            return self.bishop_logic
        elif piece_code == np.byte(5):
            return self.queen_logic
        elif piece_code == np.byte(6):
            return self.king_logic
        else:
            return None

    def pawn_logic(self, board, position):
        pass

    def rook_logic(self, board, position):
        pass

    def knight_logic(self, board, position):
        pass

    def bishop_logic(self, board, position):
        pass

    def queen_logic(self, board, position):
        pass

    def king_logic(self, board, position):
        attacked_fields = set()
        color = board[position[0], position[1]]
        row, col = position

        move_pattern_list = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col),
                             (row - 1, col - 1), (row + 1, col - 1), (row - 1, col + 1), (row + 1, col + 1)]

        for field in move_pattern_list:
            if 0 <= field[0] <= 7 and 0 <= field[1] <= 7:
                if board[field[0], field[1]] == 0:
                    attacked_fields.add(field)
                # elif field in current_player_piece_coordinates:
                #     pass
                else:
                    attacked_fields.add(field)