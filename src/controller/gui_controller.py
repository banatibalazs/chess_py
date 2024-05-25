from typing import Dict, List, Tuple, Set, Optional
from src.controller.custom_types_for_type_hinting import ByteArray8x8
import numpy as np

from src.model.utility import colors, image_paths
from src.model.utility.enums import Color
from src.model.utility.enums import GameResult
from src.view.end_game_dialog import EndGameDialog
from src.view.promotion_dialog import PromotionDialog
from src.view.chess_gui_abs import ChessGuiAbs


class GuiController:
    def __init__(self, chess_gui: ChessGuiAbs) -> None:
        self._chess_gui: ChessGuiAbs = chess_gui
        self._byte_to_piece_image_path: Dict[np.byte, str] = {
            np.byte(-6): image_paths.BL_KING_IMAGE_PATH,
            np.byte(-5): image_paths.BL_QUEEN_IMAGE_PATH,
            np.byte(-4): image_paths.BL_BISHOP_IMAGE_PATH,
            np.byte(-3): image_paths.BL_KNIGHT_IMAGE_PATH,
            np.byte(-2): image_paths.BL_ROOK_IMAGE_PATH,
            np.byte(-1): image_paths.BL_PAWN_IMAGE_PATH,

            np.byte(0): image_paths.EMPTY_SQUARE_IMAGE_PATH,

            np.byte(6): image_paths.WH_KING_IMAGE_PATH,
            np.byte(5): image_paths.WH_QUEEN_IMAGE_PATH,
            np.byte(4): image_paths.WH_BISHOP_IMAGE_PATH,
            np.byte(3): image_paths.WH_KNIGHT_IMAGE_PATH,
            np.byte(2): image_paths.WH_ROOK_IMAGE_PATH,
            np.byte(1): image_paths.WH_PAWN_IMAGE_PATH
        }

    def end_game_dialog(self, game_result: GameResult) -> None:
        dialog = EndGameDialog(game_result).wait_window()

    def get_type_from_promotion_dialog(self, color: Color) -> int:
        dialog = PromotionDialog(image_paths.WH_QUEEN_IMAGE_PATH if color == Color.W else
                                 image_paths.BL_QUEEN_IMAGE_PATH,
                                 image_paths.WH_ROOK_IMAGE_PATH if color == Color.W else
                                 image_paths.BL_ROOK_IMAGE_PATH,
                                 image_paths.WH_BISHOP_IMAGE_PATH if color == Color.W else
                                 image_paths.BL_BISHOP_IMAGE_PATH,
                                 image_paths.WH_KNIGHT_IMAGE_PATH if color == Color.W else
                                 image_paths.BL_KNIGHT_IMAGE_PATH, color)
        dialog.wait_window()
        return dialog.get_type()

    def update_labels(self, white_player_score: str, black_player_score: str,
                      snapshot_number: str, total_snapshot_number: str) -> None:
        self._chess_gui.update_labels(white_player_score, black_player_score,
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
                color = colors.LIGHT_RED_COLOR
            else:
                color = colors.DARK_RED_COLOR
            self.update_square_color([color], [[row, col]])

        if last_move is not None:
            from_row, from_col, to_row, to_col = last_move
            if (from_row + from_col) % 2 == 0:
                color = colors.LIGHT_LM_COLOR
            else:
                color = colors.DARK_LM_COLOR
            self.update_square_color([color], [[from_row, from_col]])
            if (to_row + to_col) % 2 == 0:
                color = colors.LIGHT_LM_COLOR
            else:
                color = colors.DARK_LM_COLOR
            self.update_square_color([color], [[to_row, to_col]])

        if piece_coordinate is not None:
            row, col = piece_coordinate
            if (row + col) % 2 == 0:
                color = colors.LIGHT_SELECTED_COLOR
            else:
                color = colors.DARK_SELECTED_COLOR
            self.update_square_color([color], [[row, col]])

        if possible_fields is not None:
            for field in possible_fields:
                row, col = field
                if (row + col) % 2 == 0:
                    color = colors.LIGHT_POSSIBLE_FIELD_COLOR
                else:
                    color = colors.DARK_POSSIBLE_FIELD_COLOR
                self.update_square_color([color], [[row, col]])

    def update_square_color(self, color: List[str], positions: List[List[int]]) -> None:
        for i in range(len(positions)):
            row, col = positions[i]
            self._chess_gui.update_square_color(color[i], row, col)

    def reset_square_colors(self) -> None:
        for i in range(8):
            for j in range(8):
                self._chess_gui.update_square_color(colors.WHITE_COLOR
                                                    if (i + j) % 2 == 0
                                                    else colors.BLACK_COLOR, j, i)
