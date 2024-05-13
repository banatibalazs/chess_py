import unittest
from src.model.Board import Board
from src.model.Color import Color
from src.model.King import King
from src.model.Pawn import Pawn
from src.model.PieceType import PieceType
from src.model.Player import Player
from src.model.Rook import Rook

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

class TestBishop(unittest.TestCase):

    def setUp(self):
        self.rook = Rook(Color.WHITE, 0, 0)
        self.board = Board()
        self.white_player = Player("White", Color.WHITE, self.board)
        self.black_player = Player("Black", Color.BLACK, self.board)


    def test_update_attacked_fields_rook_on_00_empty_board(self):
        self.rook.coordinates = (0, 0)
        self.rook.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                           (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)}
        self.assertEqual(self.rook._attacked_fields, expected_result)

    def test_update_attacked_fields_rook_on_07_empty_board(self):
        self.rook.coordinates = (0, 7)
        self.rook.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0),
                           (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)}
        self.assertEqual(self.rook._attacked_fields, expected_result)

    def test_update_attacked_fields_rook_on_70_empty_board(self):
        self.rook.coordinates = (7, 0)
        self.rook.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
                           (6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0)}
        self.assertEqual(self.rook._attacked_fields, expected_result)

    def test_update_attacked_fields_rook_on_77_empty_board(self):
        self.rook.coordinates = (7, 7)
        self.rook.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(7, 6), (7, 5), (7, 4), (7, 3), (7, 2), (7, 1), (7, 0),
                           (6, 7), (5, 7), (4, 7), (3, 7), (2, 7), (1, 7), (0, 7)}
        self.assertEqual(self.rook._attacked_fields, expected_result)

    def test_update_attacked_fields_rook_on_01_empty_board(self):
        self.rook.coordinates = (0, 1)
        self.rook.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(0, 0), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                           (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)}
        self.assertEqual(self.rook._attacked_fields, expected_result)

    def test_update_attacked_fields_rook_on_10_empty_board(self):
        self.rook.coordinates = (1, 0)
        self.rook.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(0, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                           (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)}
        self.assertEqual(self.rook._attacked_fields, expected_result)

    def test_update_attacked_fields_rook_on_02_empty_board(self):
        self.rook.coordinates = (0, 2)
        self.rook.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(0, 0), (0, 1), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                           (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2)}
        self.assertEqual(self.rook._attacked_fields, expected_result)

    def test_update_attacked_fields_rook_on_06_empty_board(self):
        self.rook.coordinates = (0, 6)
        self.rook.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 7),
                           (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)}
        self.assertEqual(self.rook._attacked_fields, expected_result)

    def test_update_attacked_fields_rook_on_33_surrounded_by_opponent_pieces(self):
        self.black_player.add_piece(Pawn(Color.BLACK, 2, 3))
        self.black_player.add_piece(Pawn(Color.BLACK, 3, 2))
        self.black_player.add_piece(Pawn(Color.BLACK, 4, 3))
        self.black_player.add_piece(Pawn(Color.BLACK, 3, 4))
        self.rook.coordinates = (3, 3)
        self.rook.update_attacked_fields(current_player=self.white_player, opponent=self.black_player)
        expected_result = {(3, 2), (3, 4), (2, 3), (4, 3)}
        self.assertEqual(self.rook._attacked_fields, expected_result)

    def test_update_attacked_fields_rook_on_33_surrounded_by_own_pieces(self):
        self.white_player.add_piece(Pawn(Color.WHITE, 2, 3))
        self.white_player.add_piece(Pawn(Color.WHITE, 3, 2))
        self.white_player.add_piece(Pawn(Color.WHITE, 4, 3))
        self.white_player.add_piece(Pawn(Color.WHITE, 3, 4))
        self.rook.coordinates = (3, 3)
        self.rook.update_attacked_fields(current_player=self.white_player, opponent=self.black_player)
        expected_result = set()
        self.assertEqual(self.rook._attacked_fields, expected_result)

