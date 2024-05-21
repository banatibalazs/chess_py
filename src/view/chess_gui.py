import tkinter as tk
from typing import Callable, Optional

from src.model.enums.enums import Color
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

        if pov == Color.B:
            self._chess_board: list = self.create_board_black_pov(board_click_function)

        else:
            self._chess_board: list = self.create_board_white_pov(board_click_function)


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

    def create_board_white_pov(self, board_click_function: Callable) -> list:
        chess_board = []
        for i in range(8):
            row = []
            for j in range(8):
                square = Square(self, width=8, height=4, onclick=board_click_function, col=j, row=i)
                square.grid(row=i + 3, column=j + 1, sticky="nsew")
                square.config(bg=ChessGui.WHITE_COLOR if (i + j) % 2 == 0 else ChessGui.BLACK_COLOR)
                row.append(square)
            chess_board.append(row)
        return chess_board

    def create_board_black_pov(self, board_click_function: Callable) -> list:
        chess_board = []
        offset = 3
        for i in range(7, -1, -1):
            row = []
            for j in range(7, -1, -1):
                square = Square(self, width=8, height=4, onclick=board_click_function, col=7-j, row=7-i)
                square.grid(row=i + 3, column=j + 1, sticky="nsew")
                square.config(bg=ChessGui.WHITE_COLOR if (i + j) % 2 == 0 else ChessGui.BLACK_COLOR)
                row.append(square)
            chess_board.append(row)
        return chess_board

    def update_square_image(self, image_path: str, row: int, col: int) -> None:
        self._chess_board[row][col].set_image(image_path)

    def update_square_color(self, color: str, row: int, col: int) -> None:
        self._chess_board[row][col].set_color(color)

    def update_timer_label(self):
        pass

    def update_labels(self):
        pass
