from typing import Dict, List
from src.controller.CustomTypesForTypeHinting import ByteArray8x8, BoolArray8x8
from src.controller.GameController import GameController
import numpy as np


class ViewController:

    WH_KNIGHT_IMAGE_PATH = "../resources/images/pieces/wh_knight.png"
    WH_BISHOP_IMAGE_PATH = "../resources/images/pieces/wh_bishop.png"
    WH_ROOK_IMAGE_PATH = "../resources/images/pieces/wh_rook.png"
    WH_QUEEN_IMAGE_PATH = "../resources/images/pieces/wh_queen.png"
    WH_KING_IMAGE_PATH = "../resources/images/pieces/wh_king.png"
    WH_PAWN_IMAGE_PATH = "../resources/images/pieces/wh_pawn.png"

    BL_KNIGHT_IMAGE_PATH = "../resources/images/pieces/bl_knight.png"
    BL_BISHOP_IMAGE_PATH = "../resources/images/pieces/bl_bishop.png"
    BL_ROOK_IMAGE_PATH = "../resources/images/pieces/bl_rook.png"
    BL_QUEEN_IMAGE_PATH = "../resources/images/pieces/bl_queen.png"
    BL_KING_IMAGE_PATH = "../resources/images/pieces/bl_king.png"
    BL_PAWN_IMAGE_PATH = "../resources/images/pieces/bl_pawn.png"

    EMPTY_SQUARE_IMAGE_PATH = "../resources/images/welcome_page/empty.png"

    DARK_GREEN = "#70b975"
    LIGHT_GREEN = "#aaffaf"
    LIGHT_SELECTED_COLOR = "#e0c097"
    DARK_SELECTED_COLOR = "#c29977"
    WHITE_COLOR = "#ffffff"
    BLACK_COLOR = "#4a3434"
    LIGHT_RED_COLOR = "#ff2222"
    DARK_RED_COLOR = "#ff8888"
    LIGHT_BLUE_COLOR = "#2222ff"
    DARK_BLUE_COLOR = "#8888ff"

    def __init__(self, chess_window, white_player_name: str, black_player_name: str):
        self._chess_window = chess_window
        self._int_to_piece_image_path: Dict[np.byte, str] = {
            -6: ViewController.BL_KING_IMAGE_PATH,
            -5: ViewController.BL_QUEEN_IMAGE_PATH,
            -4: ViewController.BL_BISHOP_IMAGE_PATH,
            -3: ViewController.BL_KNIGHT_IMAGE_PATH,
            -2: ViewController.BL_ROOK_IMAGE_PATH,
            -1: ViewController.BL_PAWN_IMAGE_PATH,

            0: ViewController.EMPTY_SQUARE_IMAGE_PATH,

            6: ViewController.WH_KING_IMAGE_PATH,
            5: ViewController.WH_QUEEN_IMAGE_PATH,
            4: ViewController.WH_BISHOP_IMAGE_PATH,
            3: ViewController.WH_KNIGHT_IMAGE_PATH,
            2: ViewController.WH_ROOK_IMAGE_PATH,
            1: ViewController.WH_PAWN_IMAGE_PATH
        }
        self._game_controller: GameController = GameController(white_player_name, black_player_name, self)

    def click_on_board(self, row: int, col: int) -> None:
        self._game_controller.click_on_board(row, col)

    def top_right_button_click(self) -> None:
        self._game_controller.top_right_button_click()

    def bottom_right_button_click(self) -> None:
        self._game_controller.bottom_right_button_click()

    def top_left_button_click(self) -> None:
        self._game_controller.top_left_button_click()

    def bottom_left_button_click(self) -> None:
        self._game_controller.bottom_left_button_click()

    def show_black_attack_board(self, attack_board: BoolArray8x8) -> None:

        self.reset_square_colors()

        rows, cols = np.where(attack_board == True)
        # Create a list of colors according to the original square colors
        colors = np.where((rows + cols) % 2 == 0,
                          ViewController.LIGHT_RED_COLOR,
                          ViewController.DARK_RED_COLOR).tolist()
        # Create a list of positions
        positions = np.dstack((rows, cols)).reshape(-1, 2).tolist()
        self.update_square_color(colors, positions)

    def show_white_attack_board(self, attack_board: BoolArray8x8) -> None:

            self.reset_square_colors()

            rows, cols = np.where(attack_board == True)
            # Create a list of colors according to the original square colors
            colors = np.where((rows + cols) % 2 == 0,
                            ViewController.LIGHT_GREEN,
                            ViewController.DARK_GREEN).tolist()
            # Create a list of positions
            positions = np.dstack((rows, cols)).reshape(-1, 2).tolist()
            self.update_square_color(colors, positions)

    def update_labels(self, white_player_piece_number: str, black_player_piece_number: str) -> None:
        self._chess_window.update_labels(white_player_piece_number, black_player_piece_number)

    def update_pieces_on_board(self, piece_positions_board: ByteArray8x8) -> None:
        for row in range(8):
            for col in range(8):
                path = self._int_to_piece_image_path[piece_positions_board[row][col]]
                self._chess_window.update_square_image(path, row, col)

    def update_board_coloring(self, piece_coordinate, possible_fields) -> None:

        # Reset the square colors
        self.reset_square_colors()

        if piece_coordinate is not None:
            row, col = piece_coordinate
            if (row + col) % 2 == 0:
                color = ViewController.LIGHT_SELECTED_COLOR
            else:
                color = ViewController.DARK_SELECTED_COLOR
            self.update_square_color([color], [[row, col]])

        if possible_fields is not None:
            for field in possible_fields:
                row, col = field
                if (row + col) % 2 == 0:
                    color = ViewController.LIGHT_GREEN
                else:
                    color = ViewController.DARK_GREEN
                self.update_square_color([color], [[row, col]])

    def update_square_color(self, color: List[str], positions: List[List[int]]) -> None:
        for i in range(len(positions)):
            row, col = positions[i]
            self._chess_window.update_square_color(color[i], row, col)

    def reset_square_colors(self) -> None:
        for i in range(8):
            for j in range(8):
                self._chess_window.update_square_color(ViewController.WHITE_COLOR
                                                       if (i + j) % 2 == 0
                                                       else ViewController.BLACK_COLOR, j, i)

    def right_click_on_board(self, row, col):
        print("Right click on board at row: ", row, " col: ", col)


