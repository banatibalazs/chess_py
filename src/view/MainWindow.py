import tkinter as tk
from tkinter import ttk
from typing import Callable

from PIL import Image, ImageTk
from src.controller.Game import Game
from src.model.enums.PlayerType import PlayerType


class MainWindow:

    CHESS_GAME_IMAGE_PATH = "../resources/images/welcome_page/chess-draw.png"
    START_BUTTON_IMAGE_PATH = "../resources/images/welcome_page/start.png"
    CHESS_CLOCK_IMAGE_PATH = "../resources/images/welcome_page/chess-clock.png"
    EMPTY_IMAGE_PATH = "../resources/images/welcome_page/empty.png"
    WINDOWS_ICON_PATH = "../resources/images/icon/chess.ico"
    WHITE_KING_IMAGE_PATH = "../resources/images/pieces/wh_king.png"
    BLACK_KING_IMAGE_PATH = "../resources/images/pieces/bl_king.png"
    AI_IMAGE_PATH = "../resources/images/welcome_page/ai.png"

    TEXT_SIZE = 14
    PADY = (10, 10)

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Welcome to Chess Game!")
        self.root.iconbitmap(MainWindow.WINDOWS_ICON_PATH)
        self.root.configure(background="#FFFFFF")
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.configure(background="#FFFFFF")
        self.frame.pack()
        self.chess_image_label = self.add_label_with_image(MainWindow.CHESS_GAME_IMAGE_PATH,
                                                           0, 0, 2, (370, 200))
        self.white_player_name_label = self.add_label_with_image(MainWindow.WHITE_KING_IMAGE_PATH, 1, 0, 1, (70, 70))
        self.white_player_name = self.add_entry(self.frame, 'Player1', 1, 1)
        self.white_player_type = self.add_combobox(["Human", "Random", "Greedy", "Minimax", "AlphaBeta"], 1, 3, 0)

        self.black_player_name_label = self.add_label_with_image(MainWindow.BLACK_KING_IMAGE_PATH, 2, 0, 1, (70, 70))
        self.black_player_name = self.add_entry(self.frame, 'Player2', 2, 1)
        self.black_player_type = self.add_combobox(["Human", "Random", "Greedy", "Minimax", "AlphaBeta"], 2, 3, 0)

        self.timer_label = self.add_label_with_image(MainWindow.CHESS_CLOCK_IMAGE_PATH, 3, 0, 1, (55, 55))
        self.timer_box = self.add_combobox(["-", "1 min", "3 min", "5 min", "10 min", "15 min", "20 min", "25 min",
                                            "30 min", "60 min", "90 min"], 3, 1, 1)
        self.start_button = self.add_button(self.frame,"Start Game", self.open_new_window,
                                    4, 0, 2, 22, 1, "#CCFFCC")
        self.add_image_to_button(self.start_button, MainWindow.START_BUTTON_IMAGE_PATH)
        self.exit_button = self.add_button(self.frame,  "Exit", self.exit_button_click,
                                           5, 0, 2, 22, 1, "#FFFFFF")
        self.result_label = None
        self.setup_ui()

    def setup_ui(self) -> None:

        # Bind the <Enter> and <Leave> events to the button
        self.start_button.bind("<Enter>", self.on_enter_startButton)
        self.start_button.bind("<Leave>", self.on_leave_startButton)

        # Bind the <Enter> and <Leave> events to the button
        self.exit_button.bind("<Enter>", self.on_enter_exitButton)
        self.exit_button.bind("<Leave>", self.on_leave_exitButton)

    def add_combobox(self, values: list, row: int, col: int, current: int) -> ttk.Combobox:
        combobox = ttk.Combobox(self.frame, values=values, width=10, state="readonly")
        combobox.grid(row=row, column=col, sticky="w", padx=5)
        combobox.current(current)
        return combobox

    def add_checkbox(self, text: str, row: int, col: int, variable: tk.BooleanVar) -> tk.Checkbutton:
        checkbox = tk.Checkbutton(self.frame, text=text, variable=variable, onvalue=True, offvalue=False, background="#FFFFFF",
                                  font=('Helvetica', MainWindow.TEXT_SIZE))
        checkbox.grid(row=row, column=col, sticky="w", padx=5)
        return checkbox

    def add_label(self, text: str, row: int, col: int, colspan: int) -> tk.Label:
        label = tk.Label(self.frame, text=text,
                         background="#FFFFFF",
                         font=('Helvetica', MainWindow.TEXT_SIZE, 'bold'))
        label.grid(row=row, column=col, columnspan=colspan)
        return label

    def add_label_with_image(self, image_path: str, row: int, col: int, colspan: int, size: tuple) -> tk.Label:
        image = Image.open(image_path)
        image = image.resize(size)
        image_tk = ImageTk.PhotoImage(image)
        label = tk.Label(self.frame, image=image_tk, background="#FFFFFF")
        label.image = image_tk
        label.grid(row=row, column=col, columnspan=colspan)
        return label

    def add_entry(self, frame, default_value, row: int, col: int) -> tk.Entry:
        entry = tk.Entry(frame)
        entry.insert(0, default_value)
        entry.grid(row=row, column=col, sticky="w", padx=5)
        return entry

    def add_button(self, frame, text: str, command: Callable, row: int, col: int,
                   colspan: int, width: int, height: int, color: str) -> tk.Button:
        button = tk.Button(frame, text=text, command=command, background=color, foreground='black',
                           font=('Helvetica', 16), borderwidth=2, relief="groove", width= width, height=height)
        button.grid(row=row, column=col, columnspan=colspan, pady=MainWindow.PADY)
        return button

    def add_image_to_button(self, button, image_path: str):
        image = Image.open(image_path)
        image = image.resize((60, 60))
        image_tk = ImageTk.PhotoImage(image)
        button.config(image=image_tk,  width="270", height="80")
        button.image = image_tk

    def open_new_window(self):
        try:
            time: int = int(self.timer_box.get().split(" ")[0]) * 60
        except ValueError:
            time = None

        white_player_type = self.str_to_player_type(self.white_player_type.get())
        black_player_type = self.str_to_player_type(self.black_player_type.get())

        game = Game("Chess Game", self.white_player_name.get(), white_player_type,
                    self.black_player_name.get(), black_player_type, time)
        # game.run()

    def str_to_player_type(self, player_type: str) -> PlayerType:
        if player_type == "Human":
            return PlayerType.HUMAN
        elif player_type == "Random":
            return PlayerType.RANDOM
        elif player_type == "Greedy":
            return PlayerType.GREEDY
        elif player_type == "Minimax":
            return PlayerType.MINIMAX
        elif player_type == "AlphaBeta":
            return PlayerType.MINIMAX_WITH_ALPHABETA

    def run(self):
        self.root.mainloop()

    def exit_button_click(self):
        self.root.destroy()

    def on_enter_startButton(self, event):
        # Change the style of the button when the mouse pointer enters it
        event.widget.config(background="#88FF88")

    def on_leave_startButton(self, event):
        # Change the style of the button back to the original when the mouse pointer leaves it
        event.widget.config(background="#CCFFCC")

    def on_enter_exitButton(self, event):
        # Change the style of the button when the mouse pointer enters it
        event.widget.config(background="#FFBBBB")

    def on_leave_exitButton(self, event):
        # Change the style of the button back to the original when the mouse pointer leaves it
        event.widget.config(background="#FFFFFF")



