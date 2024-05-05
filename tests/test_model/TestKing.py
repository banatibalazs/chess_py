import unittest
from src.model.Bishop import Bishop
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.King import King
from src.model.Pawn import Pawn
from src.model.Player import Player

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

class TestKing(unittest.TestCase):
    def setUp(self):
        self.king = King(ColorEnum.WHITE, 0, 0)
        self.board = Board()
        self.white_player = Player("White", ColorEnum.WHITE, self.board)
        self.black_player = Player("Black", ColorEnum.BLACK, self.board)

    def test_update_attacked_fields_king_on_00_empty_board(self):
        self.king.coordinates = (0, 0)
        self.king.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(0, 1), (1, 0), (1, 1)}
        self.assertEqual(self.king._attacked_fields, expected_result)

    def test_update_attacked_fields_king_on_07_empty_board(self):
        self.king.coordinates = (0, 7)
        self.king.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(0, 6), (1, 6), (1, 7)}
        self.assertEqual(self.king._attacked_fields, expected_result)

    def test_update_attacked_fields_king_on_70_empty_board(self):
        self.king.coordinates = (7, 0)
        self.king.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(6, 0), (6, 1), (7, 1)}
        self.assertEqual(self.king._attacked_fields, expected_result)

    def test_update_attacked_fields_king_on_77_empty_board(self):
        self.king.coordinates = (7, 7)
        self.king.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(6, 6), (6, 7), (7, 6)}
        self.assertEqual(self.king._attacked_fields, expected_result)

    def test_update_attacked_fields_king_on_33_empty_board(self):
        self.king.coordinates = (3, 3)
        self.king.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)}
        self.assertEqual(self.king._attacked_fields, expected_result)



