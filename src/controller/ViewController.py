from src.controller.GameController import GameController


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

    def __init__(self, chess_window, white_player_name, black_player_name):
        self._chess_window = chess_window
        self._previous_click = None
        self._int_to_piece_image_path = {
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
        self._game_controller = GameController(white_player_name, black_player_name, self)

    def click(self, x, y):
        print(f"Button clicked at ({x}, {y})")
        self._current_click = (x, y)
        self._game_controller.click_on_square(x, y)
        # self.print_click_on_board(x, y)
        self._previous_click = (x, y)

    def update_board(self, piece_positions_board):
        for i in range(8):
            for j in range(8):
                path = self._int_to_piece_image_path[piece_positions_board[i][j]]
                self._chess_window.update_square_image(path, i, j)


    def update_square_color(self, color, x, y):
        self._chess_window.update_square_color(color, x, y)

    def deselect_square(self, x, y):
        self._chess_window.update_square_color("white" if (x + y) % 2 == 0 else "#434343", x, y)

    def select_square(self, x, y):
        self._chess_window.update_square_color("red", x, y)
