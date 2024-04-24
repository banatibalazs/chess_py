import tkinter as tk
from PIL import Image, ImageTk

from src.controller.ViewController import ViewController
from src.model.Square import Square


class ChessWindow:



    def __init__(self, title, white_player_name, black_player_name):
        self.title = title
        self.root = tk.Toplevel()
        self.root.title(self.title)
        self._chess_board = []
        self.setup_ui()
        self.view_controller = ViewController(self, white_player_name, black_player_name)

    def setup_ui(self):
        # Create the chess board
        for i in range(8):
            row = []
            for j in range(8):
                # Create a button for each square
                square = Square(self.root,
                                width=12,
                                height=6,
                                onclick=self.onclick,
                                x=i,
                                y=j)
                square.grid(row=i, column=j, sticky="nsew")

                # Alternate the button color to create a checker pattern
                if (i + j) % 2 == 0:
                    square.config(bg='white')
                else:
                    square.config(bg='#434343')

                row.append(square)
            self._chess_board.append(row)

    def get_chess_board(self):
        return self._chess_board

    def onclick(self, x, y):
        self.view_controller.click(x, y)

    def run(self):
        self.root.mainloop()

    def update_square_image(self, image_path, x, y):
        self._chess_board[x][y].set_image(image_path)

    def update_square_color(self, color, x, y):
        self._chess_board[x][y].set_color(color)


