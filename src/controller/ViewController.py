from typing import Dict
from numpy.typing import NDArray
from src.controller.GameController import GameController
import src.view.ChessWindow as ChessWindow
import numpy as np


# from src.view.ChessWindow import ChessWindow

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

    def __init__(self, chess_window: ChessWindow, white_player_name: str, black_player_name: str):
        self._chess_window: ChessWindow = chess_window
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

    def click(self, x: int, y: int) -> None:
        self._game_controller.click_on_square(x, y)

    def update_board_view(self, piece_positions_board: NDArray[np.byte], coloring_board: NDArray[np.str_]) -> None:

        for i in range(8):
            for j in range(8):
                path = self._int_to_piece_image_path[piece_positions_board[i][j]]
                self._chess_window.update_square_image(path, i, j)

                if coloring_board[i][j] == 'X':
                    self.update_square_color(ViewController.LIGHT_SELECTED_COLOR if (i + j) % 2 == 0 else
                                             ViewController.DARK_SELECTED_COLOR, i, j)

                elif coloring_board[i][j] == 'P':
                    self.update_square_color(ViewController.LIGHT_GREEN if (i + j) % 2 == 0 else
                                             ViewController.DARK_GREEN, i, j)

                else:
                    self._chess_window.update_square_color(
                        ViewController.WHITE_COLOR if (i + j) % 2 == 0 else ViewController.BLACK_COLOR, i, j)

    def update_square_color(self, color, x: int, y: int) -> None:
        self._chess_window.update_square_color(color, x, y)
