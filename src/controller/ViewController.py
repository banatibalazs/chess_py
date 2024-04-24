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
        self.print_click_on_board(x, y)

    def update_board(self, board):
        for i in range(8):
            for j in range(8):
                path = self._int_to_piece_image_path[board[i][j]]
                self._chess_window.get_chess_board()[i][j].set_image(path)


        self.draw_board( board)

    def draw_board(self, board):
        for row in board:
            for square in row:
                print("[",square, end="]")
            print("\n")

    def print_click_on_board(self, x, y):

        board = [["[ ]" for i in range(8)] for j in range(8)]
        # Set the clicked square
        board[x][y] = "[x]"

        # Print the chess board
        for row in board:
            print(" ".join(row))


