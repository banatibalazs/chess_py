from typing import Dict, List, Tuple, Set, Optional
from src.controller.CustomTypesForTypeHinting import ByteArray8x8, BoolArray8x8
import numpy as np
from src.model.Color import Color
from src.view.ChessGui import ChessGui
from src.view.PromotionDialog import PromotionDialog


class GuiController:
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
    BLACK_COLOR = "#5f4f24"
    LIGHT_RED_COLOR = "#ff2222"
    DARK_RED_COLOR = "#ff8888"
    LIGHT_BLUE_COLOR = "#2222ff"
    DARK_BLUE_COLOR = "#8888ff"
    # Last move color
    LIGHT_LM_COLOR = "#caca7a"
    DARK_LM_COLOR = "#949434"

    def __init__(self, chess_gui: ChessGui) -> None:
        self._chess_gui: ChessGui = chess_gui
        self._byte_to_piece_image_path: Dict[np.byte, str] = {
            np.byte(-6): GuiController.BL_KING_IMAGE_PATH,
            np.byte(-5): GuiController.BL_QUEEN_IMAGE_PATH,
            np.byte(-4): GuiController.BL_BISHOP_IMAGE_PATH,
            np.byte(-3): GuiController.BL_KNIGHT_IMAGE_PATH,
            np.byte(-2): GuiController.BL_ROOK_IMAGE_PATH,
            np.byte(-1): GuiController.BL_PAWN_IMAGE_PATH,

            np.byte(0): GuiController.EMPTY_SQUARE_IMAGE_PATH,

            np.byte(6): GuiController.WH_KING_IMAGE_PATH,
            np.byte(5): GuiController.WH_QUEEN_IMAGE_PATH,
            np.byte(4): GuiController.WH_BISHOP_IMAGE_PATH,
            np.byte(3): GuiController.WH_KNIGHT_IMAGE_PATH,
            np.byte(2): GuiController.WH_ROOK_IMAGE_PATH,
            np.byte(1): GuiController.WH_PAWN_IMAGE_PATH
        }
    def get_promotion_dialog(self, color: Color) -> PromotionDialog:
        dialog = PromotionDialog(GuiController.WH_QUEEN_IMAGE_PATH if color == Color.WHITE else
                                 GuiController.BL_QUEEN_IMAGE_PATH,
                                 GuiController.WH_ROOK_IMAGE_PATH if color == Color.WHITE else
                                 GuiController.BL_ROOK_IMAGE_PATH,
                                 GuiController.WH_BISHOP_IMAGE_PATH if color == Color.WHITE else
                                 GuiController.BL_BISHOP_IMAGE_PATH,
                                 GuiController.WH_KNIGHT_IMAGE_PATH if color == Color.WHITE else
                                 GuiController.BL_KNIGHT_IMAGE_PATH)
        return dialog

    def show_black_attack_board(self, attack_board: BoolArray8x8) -> None:

        if attack_board is None:
            return

        self.reset_square_colors()

        rows, cols = np.where(attack_board is True)
        # Create a list of colors according to the original square colors
        colors = np.where((rows + cols) % 2 == 0,
                          GuiController.LIGHT_RED_COLOR,
                          GuiController.DARK_RED_COLOR).tolist()
        # Create a list of positions
        positions = np.dstack((rows, cols)).reshape(-1, 2).tolist()
        self.update_square_color(colors, positions)

    def show_white_attack_board(self, attack_board: BoolArray8x8) -> None:

        if attack_board is None:
            return

        self.reset_square_colors()

        rows, cols = np.where(attack_board is True)
        # Create a list of colors according to the original square colors
        colors = np.where((rows + cols) % 2 == 0,
                          GuiController.LIGHT_GREEN,
                          GuiController.DARK_GREEN).tolist()
        # Create a list of positions
        positions = np.dstack((rows, cols)).reshape(-1, 2).tolist()
        self.update_square_color(colors, positions)

    def update_labels(self, white_player_piece_number: str, black_player_piece_number: str,
                      snapshot_number: str, total_snapshot_number: str) -> None:
        self._chess_gui.update_labels(white_player_piece_number, black_player_piece_number,
                                      snapshot_number, total_snapshot_number)

    def update_timer_label(self, time: int, color: Color) -> None:
        self._chess_gui.update_timer_label(time, color)

    def update_pieces_on_board(self, piece_positions_board: ByteArray8x8) -> None:
        for row in range(8):
            for col in range(8):
                path = self._byte_to_piece_image_path[piece_positions_board[row][col]]
                self._chess_gui.update_square_image(path, row, col)

    def update_board_coloring(self, piece_coordinate: Optional[Tuple[int, int]],
                              possible_fields: Optional[Set[Tuple[int, int]]],
                              last_move: Optional[Tuple[int, int, int, int]],
                              checked_king_coordinates: Optional[Tuple[int, int]]) -> None:

        # Reset the square colors
        self.reset_square_colors()
        if checked_king_coordinates is not None:
            row, col = checked_king_coordinates
            if (row + col) % 2 == 0:
                color = GuiController.LIGHT_RED_COLOR
            else:
                color = GuiController.DARK_RED_COLOR
            self.update_square_color([color], [[row, col]])

        if last_move is not None:
            from_row, from_col, to_row, to_col = last_move
            if (from_row + from_col) % 2 == 0:
                color = GuiController.LIGHT_LM_COLOR
            else:
                color = GuiController.DARK_LM_COLOR
            self.update_square_color([color], [[from_row, from_col]])
            if (to_row + to_col) % 2 == 0:
                color = GuiController.LIGHT_LM_COLOR
            else:
                color = GuiController.DARK_LM_COLOR
            self.update_square_color([color], [[to_row, to_col]])

        if piece_coordinate is not None:
            row, col = piece_coordinate
            if (row + col) % 2 == 0:
                color = GuiController.LIGHT_SELECTED_COLOR
            else:
                color = GuiController.DARK_SELECTED_COLOR
            self.update_square_color([color], [[row, col]])

        if possible_fields is not None:
            for field in possible_fields:
                row, col = field
                if (row + col) % 2 == 0:
                    color = GuiController.LIGHT_GREEN
                else:
                    color = GuiController.DARK_GREEN
                self.update_square_color([color], [[row, col]])

    def update_square_color(self, color: List[str], positions: List[List[int]]) -> None:
        for i in range(len(positions)):
            row, col = positions[i]
            self._chess_gui.update_square_color(color[i], row, col)

    def reset_square_colors(self) -> None:
        for i in range(8):
            for j in range(8):
                self._chess_gui.update_square_color(GuiController.WHITE_COLOR
                                                    if (i + j) % 2 == 0
                                                    else GuiController.BLACK_COLOR, j, i)
