import tkinter as tk

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

        self.setup_ui(white_player_name, black_player_name)
        self.view_controller = ViewController(self, white_player_name, black_player_name)

    def setup_ui(self, white_player_name: str, black_player_name: str):

        self.root.minsize(688, 780)
        # Make the window adapt to its content
        self.root.geometry("")

        self.reset_button = tk.Button(self.root, text="Reset Color", command=self.reset_color_click,
                                      background="#FFFFFF", foreground='black', font=('Helvetica', 16),
                                      borderwidth=2, relief="groove", width=10, height=1)
        self.reset_button.grid(row=0, column=0, columnspan=4, pady=10)

        self.black_button = tk.Button(self.root, text="Black", command=self.black_button_click,
                                      background="#FFFFFF", foreground='black', font=('Helvetica', 16),
                                      borderwidth=2, relief="groove", width=5, height=1)
        self.black_button.grid(row=0, column=7, columnspan=2, pady=10)

        self.black_player_name_label = tk.Label(self.root, text=black_player_name, background=ChessWindow.WHITE_COLOR,
                                                font=('Helvetica', 15, 'bold'))
        self.black_player_name_label.grid(row=0, column=5, columnspan=1, sticky="nw", pady=10)

        # Create the chess board
        for i in range(0, 8, 1):
            row = []
            for j in range(8):
                # Create a button for each square
                square = Square(self.root, width=8, height=4, onclick=self.onclick, x=j, y=i)
                square.grid(row=i + 1, column=j + 1, sticky="nsew")

                # Alternate the button color to create a checker pattern
                square.config(bg=ChessWindow.WHITE_COLOR if (i + j) % 2 == 0 else ChessWindow.BLACK_COLOR)

                row.append(square)
            self._chess_board.append(row)

        self.white_player_name_label = tk.Label(self.root, text=white_player_name, background=ChessWindow.WHITE_COLOR,
                                                font=('Helvetica', 15, 'bold'))
        self.white_player_name_label.grid(row=10, column=5, columnspan=1, sticky="sw", pady=10)

        self.white_button = tk.Button(self.root, text="White", command=self.white_button_click,
                                      background="#FFFFFF", foreground='black', font=('Helvetica', 16),
                                      borderwidth=2, relief="groove", width=5, height=1)
        self.white_button.grid(row=10, column=7, columnspan=2, pady=10)

        self.extra_button = tk.Button(self.root, text="Extra", command=self.extra_button_click,
                                      background="#FFFFFF", foreground='black', font=('Helvetica', 16),
                                      borderwidth=2, relief="groove", width=10, height=1)
        self.extra_button.grid(row=10, column=0, columnspan=4, pady=10)

    def black_button_click(self):
        self.view_controller.black_button_click()

    def white_button_click(self):
        self.view_controller.white_button_click()

    def reset_color_click(self):
        self.view_controller.reset_button_click()

    def extra_button_click(self):
        self.view_controller.extra_button_click()

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
