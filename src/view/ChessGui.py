import tkinter as tk
from typing import Callable, Optional

from src.model.Color import Color
from src.model.Square import Square


class ChessGui(tk.Toplevel):
    BLACK_COLOR = "#111111"
    WHITE_COLOR = "#ffffff"

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
        self.minsize(688, 780)
        self.geometry("")
        self.configure(background="#FFFFFF")
        self.white_player_name_label: Optional[tk.Label] = self.add_label(black_player_name, 0, 1, 1, 10)
        self.black_player_score_label: Optional[tk.Label] = self.add_label("16", 0, 2, 1, 10)
        self.black_player_timer_label: Optional[tk.Label] = self.add_label(self.time, 0, 3, 1, 10)
        self.top_left_button: Optional[tk.Button] = self.add_button("Top left", top_left_button_click_function, 0, 4, 2, 10)
        self.top_right_button: Optional[tk.Button] = self.add_button("Top right",top_right_button_click_function, 0, 7, 2, 10)
        self._chess_board: list = self.create_board(board_click_function)
        self.black_player_name_label: Optional[tk.Label] = self.add_label(white_player_name, 10, 1, 1, 10)
        self.white_player_score_label: Optional[tk.Label] = self.add_label("16", 10, 2, 1, 10)
        self.white_player_timer_label: Optional[tk.Label] = self.add_label(self.time, 10, 3, 1, 10)
        self.bottom_left_button: Optional[tk.Button] = self.add_button("<",bottom_left_button_click_function, 10, 4, 2, 10)
        self.snapshot_label: Optional[tk.Label] = self.add_label("1/1", 10, 6, 1, 10)
        self.bottom_right_button: Optional[tk.Button] = self.add_button(">", bottom_right_button_click_function, 10, 7, 2, 10)

    def add_button(self, text: str, command: Callable, row: int, column: int, columnspan: int, pady: int) -> tk.Button:
        button = tk.Button(self, text=text, command=command, background="#F1F1F1", foreground='black',
                           font=('Helvetica', 16), borderwidth=0, relief="groove", width=7, height=1)
        button.grid(row=row, column=column, columnspan=columnspan, pady=pady)
        return button

    def add_label(self, text: str, row: int, column: int, columnspan: int, pady: int) -> tk.Label:
        label = tk.Label(self, text=text, background="#FFFFFF", font=('Helvetica', 16))
        label.grid(row=row, column=column, columnspan=columnspan, pady=pady)
        return label

    def create_board(self, board_click_function: Callable) -> list:
        chess_board = []
        for i in range(8):
            row = []
            for j in range(8):
                square = Square(self, width=8, height=4, onclick=board_click_function, col=j, row=i)
                square.grid(row=i + 1, column=j + 1, sticky="nsew")
                square.config(bg=ChessGui.WHITE_COLOR if (i + j) % 2 == 0 else ChessGui.BLACK_COLOR)
                row.append(square)
            chess_board.append(row)
        return chess_board

    def update_square_image(self, image_path: str, row: int, col: int) -> None:
        self._chess_board[row][col].set_image(image_path)

    def update_square_color(self, color: str, row: int, col: int) -> None:
        self._chess_board[row][col].set_color(color)

    def update_labels(self, white_player_piece_number: str, black_player_piece_number: str,
                      snapshot_number: str, total_snapshot_number: str) -> None:
        self.white_player_score_label.config(text=white_player_piece_number)
        self.black_player_score_label.config(text=black_player_piece_number)
        self.snapshot_label.config(text=f"{snapshot_number}/{total_snapshot_number}")

    def update_timer_label(self, time: int, color: Color) -> None:
        (min, sec) = divmod(time, 60)
        time_str = f"{min:02d}:{sec:02d}"
        if color == Color.WHITE:
            self.white_player_timer_label.config(text=time_str)
        else:
            self.black_player_timer_label.config(text=time_str)
