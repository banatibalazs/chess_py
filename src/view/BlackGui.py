import tkinter as tk
from typing import Callable, Optional

from src.model.Color import Color
from src.view.Square import Square


class BlackGui(tk.Toplevel):
    BLACK_COLOR = "#111111"
    WHITE_COLOR = "#ffffff"
    WINDOWS_ICON_PATH = "../resources/images/icon/chess.ico"
    BUTTON_COLOR = "#e0ffe0"
    BUTTON_COLOR_HOVER = "#a3ffa3"
    LABEL_FOREGROUND_COLOR = "#ffffff"
    BUTTON_FOREGROUND_COLOR = "#000000"

    def __init__(self, title, white_player_name: str, black_player_name: str, time: Optional[int], board_click_function: Callable,
                 top_left_button_click_function: Callable, top_right_button_click_function: Callable,
                 bottom_right_button_click_function: Callable, bottom_left_button_click_function: Callable):
        tk.Toplevel.__init__(self)
        if time is None:
            self.time = " "
        else:
            (min, sec) = divmod(time, 60)
            self.time = f"{min:02d}:{sec:02d}"
        self.title(title)
        self.iconbitmap(BlackGui.WINDOWS_ICON_PATH)
        self.minsize(688, 780)
        self.geometry("")
        self.configure(background="#000000")
        self.black_player_name_label: Optional[tk.Label] = self.add_label(black_player_name,11, 1, 3, 10)
        self.black_player_score_label: Optional[tk.Label] = self.add_label("Score:",11, 4, 2, 10)
        self.black_player_timer_label: Optional[tk.Label] = self.add_label(f"Time: {self.time}",11, 7, 2, 10)

        self._chess_board: list = self.create_board(board_click_function)

        self.white_player_name_label: Optional[tk.Label] = self.add_label(white_player_name,1, 1, 3, 10)
        self.white_player_score_label: Optional[tk.Label] = self.add_label("Score",1, 4, 2, 10)
        self.bottom_left_button: Optional[tk.Button] = self.add_button("<",bottom_left_button_click_function,
                                                                       6, 0, 1, 2, 10, 15, 3, 3)
        self.snapshot_label: Optional[tk.Label] = self.add_label("1/1",14, 8, 3, 10)
        self.bottom_right_button: Optional[tk.Button] = self.add_button(">", bottom_right_button_click_function,6, 10, 1, 2, 10, 15, 3, 3)
        self.white_player_timer_label: Optional[tk.Label] = self.add_label(f"Time: {self.time}",1, 7, 2, 10)

    def add_button(self, text: str, command: Callable, row: int, column: int, columnspan: int, row_span: int,
                   pady: int, padx: int = 0, width: int = 7, height: int = 1) -> tk.Button:
        button = tk.Button(self, text=text, command=command, background=BlackGui.BUTTON_COLOR, foreground=BlackGui.BUTTON_FOREGROUND_COLOR,
                           font=('Helvetica', 12, 'bold'), borderwidth=1, relief="ridge", width=width, height=height)
        button.grid(row=row, column=column, columnspan=columnspan, rowspan=row_span, pady=pady, padx=padx)
        button.bind("<Enter>", self.on_enter)
        button.bind("<Leave>", self.on_leave)
        return button

    def on_enter(self, event) -> None:
        event.widget.config(background=BlackGui.BUTTON_COLOR_HOVER)

    def on_leave(self, event) -> None:
        event.widget.config(background=BlackGui.BUTTON_COLOR)

    def add_label(self, text: str, row: int, column: int, columnspan: int, pady: int) -> tk.Label:
        label = tk.Label(self, text=text, background="#000000", font=('Helvetica', 12), fg=BlackGui.LABEL_FOREGROUND_COLOR)
        label.grid(row=row, column=column, columnspan=columnspan, pady=pady)
        return label

    def create_board(self, board_click_function: Callable) -> list:
        chess_board = []
        offset = 3
        for i in range(7,-1,-1):
            row = []
            for j in range(7,-1,-1):
                square = Square(self, width=8, height=4, onclick=board_click_function, col=7-j, row=7-i)
                square.grid(row=i + 3, column=j + 1, sticky="nsew")
                square.config(bg=BlackGui.WHITE_COLOR if (i + j) % 2 == 0 else BlackGui.BLACK_COLOR)
                row.append(square)
            chess_board.append(row)
        return chess_board

    def update_square_image(self, image_path: str, row: int, col: int) -> None:
        self._chess_board[row][col].set_image(image_path)

    def update_square_color(self, color: str, row: int, col: int) -> None:
        self._chess_board[row][col].set_color(color)

    def update_labels(self, white_player_piece_number: str, black_player_piece_number: str,
                      snapshot_number: str, total_snapshot_number: str) -> None:
        self.white_player_score_label.config(text=f"Score: {white_player_piece_number}")
        self.black_player_score_label.config(text=f"Score: {black_player_piece_number}")
        self.snapshot_label.config(text=f"{snapshot_number}/{total_snapshot_number}")

    def update_timer_label(self, time: int, color: Color) -> None:
        (min, sec) = divmod(time, 60)
        time_str = f"{min:02d}:{sec:02d}"
        if color == Color.WHITE:
            self.white_player_timer_label.config(text=f"Time: {time_str}")
        else:
            self.black_player_timer_label.config(text=f"Time: {time_str}")
