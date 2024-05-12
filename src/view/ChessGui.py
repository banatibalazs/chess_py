import tkinter as tk
from typing import Callable

from src.model.Square import Square


class ChessGui(tk.Toplevel):
    BLACK_COLOR = "#4a3434"
    WHITE_COLOR = "#ffffff"

    def __init__(self, title, white_player_name, black_player_name, board_click_function: Callable,
                 top_left_button_click_function: Callable, top_right_button_click_function: Callable,
                    bottom_right_button_click_function: Callable, bottom_left_button_click_function: Callable):
        tk.Toplevel.__init__(self)
        self.title("Welcome to Chess Game!")
        self.configure(background="#FFFFFF")
        self.white_player_name_label = None
        self.black_player_name_label = None
        self._chess_board: list = []
        self.top_left_button = None
        self.top_right_button = None
        self.bottom_right_button = None
        self.bottom_left_button = None
        self.result_label = None
        self.setup_ui(white_player_name, black_player_name,
                      board_click_function, top_left_button_click_function,
                      top_right_button_click_function, bottom_right_button_click_function,
                      bottom_left_button_click_function)

    def setup_ui(self, white_player_name: str, black_player_name: str,
                 board_click_function: Callable, top_left_button_click_function: Callable,
                 top_right_button_click_function: Callable, bottom_right_button_click_function: Callable,
                 bottom_left_button_click_function: Callable):
        self.minsize(688, 780)
        self.geometry("")
        self.top_left_button = self.add_button("Top left", top_left_button_click_function, 0, 0, 4, 10)
        self.top_right_button = self.add_button("Top right",top_right_button_click_function, 0, 7, 2, 10)
        self.black_player_name_label = self.add_label(black_player_name, 0, 5, 1, 10)
        self.black_player_piece_number_label = self.add_label("16", 0, 6, 1, 10)
        self.create_board(board_click_function=board_click_function)
        self.white_player_name_label = self.add_label(white_player_name, 10, 5, 1, 10)
        self.white_player_piece_number_label = self.add_label("16", 10, 6, 1, 10)
        self.bottom_right_button = self.add_button(">", bottom_right_button_click_function, 10, 7, 2, 10)
        self.bottom_left_button = self.add_button("<",bottom_left_button_click_function, 10, 0, 4, 10)

    def add_button(self, text: str, command: Callable, row: int, column: int, columnspan: int, pady: int):
        button = tk.Button(self, text=text, command=command, background="#FFFFFF", foreground='black',
                           font=('Helvetica', 16), borderwidth=2, relief="groove", width=10, height=1)
        button.grid(row=row, column=column, columnspan=columnspan, pady=pady)
        return button

    def add_label(self, text: str, row: int, column: int, columnspan: int, pady: int):
        label = tk.Label(self, text=text, background="#FFFFFF", font=('Helvetica', 16))
        label.grid(row=row, column=column, columnspan=columnspan, pady=pady)
        return label

    def create_board(self, board_click_function: Callable):
        for i in range(8):
            row = []
            for j in range(8):
                square = Square(self, width=8, height=4, onclick=board_click_function, col=j, row=i)
                square.grid(row=i + 1, column=j + 1, sticky="nsew")
                square.config(bg=ChessGui.WHITE_COLOR if (i + j) % 2 == 0 else ChessGui.BLACK_COLOR)
                row.append(square)
            self._chess_board.append(row)

    def run(self):
        self.mainloop()

    def update_square_image(self, image_path, row, col):
        self._chess_board[row][col].set_image(image_path)

    def update_square_color(self, color, row, col):
        self._chess_board[row][col].set_color(color)

    def update_labels(self, white_player_piece_number: str, black_player_piece_number: str):
        self.white_player_piece_number_label.config(text=white_player_piece_number)
        self.black_player_piece_number_label.config(text=black_player_piece_number)