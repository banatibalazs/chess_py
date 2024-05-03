import unittest
from src.model.Bishop import Bishop
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.King import King
from src.model.PieceTypeEnum import PieceTypeEnum
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

class TestBishop(unittest.TestCase):
    def setUp(self):
        self.bishop = Bishop(ColorEnum.WHITE, 0, 0)
        self.board = Board()
        self.white_player = Player("White", ColorEnum.WHITE, self.board)
        self.black_player = Player("Black", ColorEnum.BLACK, self.board)
        # self.current_player.add_piece(King(ColorEnum.WHITE, 4, 7))
        # self.opponent.add_piece(King(ColorEnum.BLACK, 4, 0))

    def test_update_attacked_fields_bishop_on_44_empty_board(self):
        self.bishop.coordinates = (4, 4)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(0, 0), (1, 1), (2, 2), (3, 3), (5, 5), (6, 6), (7, 7), (5, 3),
                           (6, 2), (7, 1), (3, 5), (2, 6), (1, 7)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_00_empty_board(self):
        self.bishop.coordinates = (0, 0)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_01_empty_board(self):
        self.bishop.coordinates = (0, 1)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (1, 0)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_02_empty_board(self):
        self.bishop.coordinates = (0, 2)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (1, 1), (2, 0)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_03_empty_board(self):
        self.bishop.coordinates = (0, 3)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(1, 4), (2, 5), (3, 6), (4, 7), (1, 2), (2, 1), (3, 0)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_04_empty_board(self):
        self.bishop.coordinates = (0, 4)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(1, 5), (2, 6), (3, 7), (1, 3), (2, 2), (3, 1), (4, 0)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_05_empty_board(self):
        self.bishop.coordinates = (0, 5)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(1, 6), (2, 7), (1, 4), (2, 3), (3, 2), (4, 1), (5, 0)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_06_empty_board(self):
        self.bishop.coordinates = (0, 6)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(1, 7), (1, 5), (2, 4), (3, 3), (4, 2), (5, 1), (6, 0)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_07_empty_board(self):
        self.bishop.coordinates = (0, 7)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_70_empty_board(self):
        self.bishop.coordinates = (7, 0)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6), (0, 7)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_71_empty_board(self):
        self.bishop.coordinates = (7, 1)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(6, 2), (5, 3), (4, 4), (3, 5), (2, 6), (1, 7), (6, 0)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_72_empty_board(self):
        self.bishop.coordinates = (7, 2)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(6, 3), (5, 4), (4, 5), (3, 6), (2, 7), (6, 1), (5, 0)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_73_empty_board(self):
        self.bishop.coordinates = (7, 3)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(6, 4), (5, 5), (4, 6), (3, 7), (6, 2), (5, 1), (4, 0)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_74_empty_board(self):
        self.bishop.coordinates = (7, 4)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(6, 5), (5, 6), (4, 7), (6, 3), (5, 2), (4, 1), (3, 0)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_75_empty_board(self):
        self.bishop.coordinates = (7, 5)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(6, 6), (5, 7), (6, 4), (5, 3), (4, 2), (3, 1), (2, 0)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_76_empty_board(self):
        self.bishop.coordinates = (7, 6)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(6, 7), (6, 5), (5, 4), (4, 3), (3, 2), (2, 1), (1, 0)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_77_empty_board(self):
        self.bishop.coordinates = (7, 7)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(6, 6), (5, 5), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_72_with_starting_board(self):
        self.white_player.init_pieces()
        self.black_player.init_pieces()

        self.white_player.remove_piece_at(2, 7)
        self.bishop.coordinates = (7, 2)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {}
        self.assertEqual(self.bishop._attacked_fields, expected_result)


if __name__ == '__main__':
    unittest.main(verbosity=1)