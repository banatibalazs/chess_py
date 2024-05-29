import tkinter as tk
from PIL import Image, ImageTk
from typing import Callable, Optional

from src.model.utility import colors
from src.model.utility.enums import Color
from src.view.square import Square
from src.view.chess_gui_abs import ChessGuiAbs


class ChessGui(ChessGuiAbs):
    BLACK_COLOR = "#111111"
    WHITE_COLOR = "#ffffff"
    WINDOWS_ICON_PATH = "../resources/images/icon/chess.ico"
    BUTTON_COLOR = "#e0ffe0"
    BUTTON_COLOR_HOVER = "#a3ffa3"
    LABEL_FOREGROUND_COLOR = "#ffffff"
    BUTTON_FOREGROUND_COLOR = "#000000"

    def __init__(self, title, pov: Color, white_player_name: str, black_player_name: str, _time: Optional[int], board_click_function: Callable,
                 bottom_right_button_click_function: Callable, bottom_left_button_click_function: Callable):
        tk.Toplevel.__init__(self)
        if _time is None:
            self.time = " "
        else:
            (min, sec) = divmod(_time, 60)
            self.time = f"{min:02d}:{sec:02d}"
        self.title(title)
        self.iconbitmap(ChessGui.WINDOWS_ICON_PATH)
        self.minsize(688, 780)
        self.geometry("")
        self.configure(background="#000000")
        self.board_click_function = board_click_function

        if pov == Color.B:
            self._chess_board: list = self.create_board_black_pov()

        else:
            self._chess_board: list = self.create_board_white_pov()

        # Add two buttons to the right of the chess board
        self.add_button("<", bottom_left_button_click_function, 11, 7, 1, 1, 40, 0, 3)
        self.add_button(">", bottom_right_button_click_function, 11, 8, 1, 1, 40, 0, 3)


    def add_button(self, text: str, command: Callable, row: int, column: int, columnspan: int, row_span: int,
                   pady: int, padx: int = 0, width: int = 7, height: int = 1) -> tk.Button:
        button = tk.Button(self, text=text, command=command, background=ChessGui.BUTTON_COLOR, foreground=ChessGui.BUTTON_FOREGROUND_COLOR,
                           font=('Helvetica', 12, 'bold'), borderwidth=1, relief="ridge", width=width, height=height)
        button.grid(row=row, column=column, columnspan=columnspan, rowspan=row_span, pady=pady, padx=padx)
        button.bind("<Enter>", self.on_enter)
        button.bind("<Leave>", self.on_leave)
        return button

    def on_enter(self, event) -> None:
        event.widget.config(background=ChessGui.BUTTON_COLOR_HOVER)

    def on_leave(self, event) -> None:
        event.widget.config(background=ChessGui.BUTTON_COLOR)

    def add_label(self, text: str, row: int, column: int, columnspan: int, pady: int) -> tk.Label:
        label = tk.Label(self, text=text, background="#000000", font=('Helvetica', 12), fg=ChessGui.LABEL_FOREGROUND_COLOR)
        label.grid(row=row, column=column, columnspan=columnspan, pady=pady)
        return label

    def create_board_white_pov(self) -> list:
        chess_board = []
        for i in range(8):
            row = []
            for j in range(8):
                # square = Square(self, width=8, height=4, onclick=board_click_function, col=j, row=i)
                square = Square(self, width=8, height=4, col=j, row=i)
                square.bind("<Button-1>", self.on_square_click)
                square.bind("<Button-3>", self.on_right_click)
                square.grid(row=i, column=j + 1, sticky="nsew")
                square.config(bg=ChessGui.WHITE_COLOR if (i + j) % 2 == 0 else ChessGui.BLACK_COLOR)
                row.append(square)
            chess_board.append(row)
        return chess_board

    def create_board_black_pov(self) -> list:
        chess_board = []
        offset = 3
        for i in range(7, -1, -1):
            row = []
            for j in range(7, -1, -1):
                # square = Square(self, width=8, height=4, onclick=board_click_function, col=7-j, row=7-i)
                square = Square(self, width=8, height=4, col=7 - j, row=7 - i)
                square.bind("<Button-1>",self.on_square_click)
                square.grid(row=i, column=j + 1, sticky="nsew")
                square.config(bg=ChessGui.WHITE_COLOR if (i + j) % 2 == 0 else ChessGui.BLACK_COLOR)
                row.append(square)
            chess_board.append(row)
        return chess_board

    def on_square_click(self, event):
        # Get the Square widget that was clicked
        square = event.widget
        # Get the row and column of the Square
        row = square.row
        col = square.col
        # Call the board_click_function with the row and column
        self.board_click_function(row, col)

    def on_right_click(self, event):
        # Get the Square widget that was clicked
        square = event.widget
        # Get the row and column of the Square
        row = square.row
        col = square.col
        # Check if the square has an attribute 'original_color'
        if not hasattr(square, 'original_color'):
            # If not, store the current color as the original color
            square.original_color = square.cget('bg')
        # Check if the square has an attribute 'toggled'
        if not hasattr(square, 'toggled'):
            # If not, set it to False
            square.toggled = False
        # If the square is toggled, set its color back to the original color
        if square.toggled:
            square.config(bg=square.original_color)
        else:
            # If the square is not toggled, change its color
            square.config(bg=colors.LIGHT_RED_COLOR if (row + col) % 2 == 0 else colors.DARK_RED_COLOR)
        # Toggle the 'toggled' attribute
        square.toggled = not square.toggled

    def set_image(self, piece_image_path, row, col):
        piece_image = Image.open(piece_image_path)
        piece_image = piece_image.resize((105, 110))
        piece_image_tk = ImageTk.PhotoImage(piece_image)  # Use ImageTk.PhotoImage here
        self._chess_board[row][
            col].image = piece_image_tk  # Keep a reference to the image to prevent it from being garbage collected
        self._chess_board[row][col].config(image=piece_image_tk, width="80", height="80")

    def update_square_image(self, image_path: str, row: int, col: int) -> None:
        # self._chess_board[row][col].set_image(image_path)
        self.set_image(image_path, row, col)

    def update_square_color(self, color: str, row: int, col: int) -> None:
        self._chess_board[row][col].set_color(color)

    def update_timer_label(self):
        pass

    def update_labels(self):
        pass
