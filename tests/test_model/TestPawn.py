import unittest
from src.model.board import Board
from src.model.enums.color import Color
from src.model.pieces.pawn import Pawn
from src.model.players.player import Player

"""
                            Black player's side
            -----------------------------------------------------------------------------

            Grid layout                       Piece codes                         Chess notation

[00][01][02][03][04][05][06][07]   [-2][-3][-4][-5][-6][-4][-3][-2]   [A8][B8][C8][D8][E8][F8][G8][H8]
[10][11][12][13][14][15][16][17]   [-1][-1][-1][-1][-1][-1][-1][-1]   [A7][B7][C7][D7][E7][F7][G7][H7]
[20][21][22][23][24][25][26][27]   [ 0][ 0][ 0][ 0][ 0][ 0][ 0][ 0]   [A6][B6][C6][D6][E6][F6][G6][H6]
[30][31][32][33][34][35][36][37]   [ 0][ 0][ 0][ 0][ 0][ 0][ 0][ 0]   [A5][B5][C5][D5][E5][F5][G5][H5]
[40][41][42][43][44][45][46][47]   [ 0][ 0][ 0][ 0][ 0][ 0][ 0][ 0]   [A4][B4][C4][D4][E4][F4][G4][H4]
[50][51][52][53][54][55][56][57]   [ 0][ 0][ 0][ 0][ 0][ 0][ 0][ 0]   [A3][B3][C3][D3][E3][F3][G3][H3]
[60][61][62][63][64][65][66][67]   [ 1][ 1][ 1][ 1][ 1][ 1][ 1][ 1]   [A2][B2][C2][D2][E2][F2][G2][H2]
[70][71][72][73][74][75][76][77]   [ 2][ 3][ 4][ 5][ 6][ 4][ 3][ 2]   [A1][B1][C1][D1][E1][F1][G1][H1]

            -----------------------------------------------------------------------------
                                             White player's side
"""

class TestPawn(unittest.TestCase):
    def setUp(self):
        self.pawn = None
        self.board = Board()
        self.white_player = Player("White", Color.WHITE, self.board)
        self.black_player = Player("Black", Color.BLACK, self.board)

    def test_update_attacked_fields_white_pawn_in_rows_0_to_7_empty_board(self):
        for j in range(8):
            for i in range(8):
                self.pawn = Pawn(Color.WHITE, j, i)
                self.pawn.update_attacked_fields(self.white_player, self.black_player)
                if j == 0:
                    expected_result = set()
                elif i == 0:
                    expected_result = {(j - 1, i + 1)}
                elif i == 7:
                    expected_result = {(j - 1, i - 1)}
                else:
                    expected_result = {(j - 1, i - 1), (j - 1, i + 1)}
                self.assertEqual(self.pawn._attacked_fields, expected_result)

    def test_update_attacked_fields_black_pawn_in_rows_0_to_7_empty_board(self):
        for row in range(8):
            for col in range(8):
                self.pawn = Pawn(Color.BLACK, row, col)
                self.pawn.update_attacked_fields(self.black_player, self.white_player)
                if row == 7:
                    expected_result = set()
                elif col == 0:
                    expected_result = {(row + 1, col + 1)}
                elif col == 7:
                    expected_result = {(row + 1, col - 1)}
                else:
                    expected_result = {(row + 1, col - 1), (row + 1, col + 1)}
                self.assertEqual(self.pawn._attacked_fields, expected_result)

    def test_white_pawn_attacked_fields_with_enemy_pieces(self):
        for row in range(8):
            for col in range(8):
                self.black_player.add_piece(Pawn(Color.BLACK, row, col))

        for row in range(8):
            for col in range(8):
                self.pawn = Pawn(Color.WHITE, row, col)
                self.pawn.update_attacked_fields(self.white_player, self.black_player)
                if row == 0:
                    expected_result = set()
                elif col == 0:
                    expected_result = {(row - 1, col + 1)}
                elif col == 7:
                    expected_result = {(row - 1, col - 1)}
                else:
                    expected_result = {(row - 1, col - 1), (row - 1, col + 1)}
                self.assertEqual(self.pawn._attacked_fields, expected_result)

    def test_black_pawn_attacked_fields_with_enemy_pieces(self):
        for row in range(8):
            for col in range(8):
                self.white_player.add_piece(Pawn(Color.WHITE, row, col))

        for row in range(8):
            for col in range(8):
                self.pawn = Pawn(Color.BLACK, row, col)
                self.pawn.update_attacked_fields(self.black_player, self.white_player)
                if row == 7:
                    expected_result = set()
                elif col == 0:
                    expected_result = {(row + 1, col + 1)}
                elif col == 7:
                    expected_result = {(row + 1, col - 1)}
                else:
                    expected_result = {(row + 1, col - 1), (row + 1, col + 1)}
                self.assertEqual(self.pawn._attacked_fields, expected_result)

    def test_white_pawn_attacked_fields_with_friendly_pieces(self):
        for row in range(8):
            for col in range(8):
                self.white_player.add_piece(Pawn(Color.WHITE, row, col))

        for row in range(8):
            for col in range(8):
                self.pawn = Pawn(Color.WHITE, row, col)
                self.pawn.update_attacked_fields(self.white_player, self.black_player)
                self.assertEqual(self.pawn._attacked_fields, set())

    def test_black_pawn_attacked_fields_with_friendly_pieces(self):
        for row in range(8):
            for col in range(8):
                self.black_player.add_piece(Pawn(Color.BLACK, row, col))

        for row in range(8):
            for col in range(8):
                self.pawn = Pawn(Color.BLACK, row, col)
                self.pawn.update_attacked_fields(self.black_player, self.white_player)
                self.assertEqual(self.pawn._attacked_fields, set())

