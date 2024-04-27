import tkinter as tk
from typing import Callable

from src.controller.ViewController import ViewController
from src.model.Square import Square


class ChessWindow:
    BLACK_COLOR = "#4a3434"
    WHITE_COLOR = "#ffffff"

    def __init__(self, title, white_player_name: str, black_player_name: str):
        self.title: str = title
        self.root = tk.Toplevel()
        self.root.title(self.title)

        self._chess_board: list = []

        self.white_player_name_label = None
        self.black_player_name_label = None

        self.white_button = None
        self.black_button = None
        self.reset_button = None
        self.extra_button = None

        self.setup_ui(white_player_name, black_player_name)
        self.view_controller = ViewController(self, white_player_name, black_player_name)

    def setup_ui(self, white_player_name: str, black_player_name: str):

        self.root.minsize(688, 780)
        # Make the window adapt to its content
        self.root.geometry("")

        self.reset_button = self.create_button("Reset", self.reset_button_click,
                                               0, 0, 4, 10)
        self.black_button = self.create_button("Black", self.black_button_click,
                                               0, 7, 2, 10)
        self.black_player_name_label = self.create_label(black_player_name,
                                               0, 5, 1, 10)

        self.create_board()

        self.white_player_name_label = self.create_label(white_player_name,
                                               10, 5, 1, 10)
        self.white_button = self.create_button("White", self.white_button_click,
                                               10, 7, 2, 10)
        self.extra_button = self.create_button("Extra", self.extra_button_click,
                                               10, 0, 4, 10)

    def create_button(self, text: str, command: Callable, row: int, column: int, columnspan: int, pady: int):
        button = tk.Button(self.root, text=text, command=command,
                           background="#FFFFFF", foreground='black', font=('Helvetica', 16),
                           borderwidth=2, relief="groove", width=10, height=1)
        button.grid(row=row, column=column, columnspan=columnspan, pady=pady)
        return button

    def create_label(self, text: str, row: int, column: int, columnspan: int, pady: int):
        label = tk.Label(self.root, text=text, background="#FFFFFF", font=('Helvetica', 16))
        label.grid(row=row, column=column, columnspan=columnspan, pady=pady)
        return label

    def create_board(self):
        for i in range(8):
            row = []
            for j in range(8):
                # Create a button for each square
                square = Square(self.root, width=8, height=4, onclick=self.onclick, x=j, y=i)
                square.grid(row=i + 1, column=j + 1, sticky="nsew")

                # Alternate the button color to create a checker pattern
                square.config(bg=ChessWindow.WHITE_COLOR if (i + j) % 2 == 0 else ChessWindow.BLACK_COLOR)

                row.append(square)
            self._chess_board.append(row)

    def black_button_click(self):
        self.view_controller.black_button_click()

    def white_button_click(self):
        self.view_controller.white_button_click()

    def reset_button_click(self):
        self.view_controller.reset_button_click()

    def extra_button_click(self):
        self.view_controller.extra_button_click()

    def get_chess_board(self):
        return self._chess_board

    def onclick(self, x, y):
        self.view_controller.click_on_board(x, y)

    def run(self):
        self.root.mainloop()

    def update_square_image(self, image_path, x, y):
        self._chess_board[x][y].set_image(image_path)

    def update_square_color(self, color, x, y):
        self._chess_board[x][y].set_color(color)
