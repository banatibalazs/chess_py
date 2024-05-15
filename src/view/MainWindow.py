import tkinter as tk
from tkinter import ttk
from typing import Callable

from PIL import Image, ImageTk
from src.controller.Game import Game


class MainWindow:

    CHESS_GAME_IMAGE_PATH = "../resources/images/welcome_page/chess-draw.png"
    START_BUTTON_IMAGE_PATH = "../resources/images/welcome_page/start.png"
    CHESS_CLOCK_IMAGE_PATH = "../resources/images/welcome_page/chess-clock.png"
    EMPTY_IMAGE_PATH = "../resources/images/welcome_page/empty.png"
    WINDOWS_ICON_PATH = "../resources/images/icon/chess.ico"
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
        self.white_player_name = self.add_entry(self.frame, 'Player1', 1, 1)
        self.black_player_name = self.add_entry(self.frame, 'Player2', 2, 1)
        self.start_button = self.add_button(self.frame,"Start Game", self.open_new_window,
                                    4, 0, 2, 22, 1, "#CCFFCC")
        self.add_image_to_button(self.start_button, MainWindow.START_BUTTON_IMAGE_PATH)
        self.exit_button = self.add_button(self.frame,  "Exit", self.exit_button_click,
                                           5, 0, 2, 22, 1, "#FFFFFF")
        self.result_label = None
        self.setup_ui()

    def setup_ui(self) -> None:

        chess_image = Image.open(MainWindow.CHESS_GAME_IMAGE_PATH)
        chess_clock_image = Image.open(MainWindow.CHESS_CLOCK_IMAGE_PATH)

        # Resize the images
        chess_image = chess_image.resize((370, 200))
        chess_clock_image = chess_clock_image.resize((55, 55))

        chess_image_tk = ImageTk.PhotoImage(chess_image)
        chess_clock_image_tk = ImageTk.PhotoImage(chess_clock_image)

        # Create a label and add the image to it
        image_label = tk.Label(self.frame, image=chess_image_tk)
        image_label.image = chess_image_tk  # keep a reference to the image
        image_label.grid(row=0, column=0, columnspan=2)

        white_player_name_label = tk.Label(self.frame, text="WhitePlayer:",
                                        background="#FFFFFF",
                                        font=('Helvetica', MainWindow.TEXT_SIZE, 'bold'))
        white_player_name_label.grid(row=1, column=0, sticky="e", pady=MainWindow.PADY)

        black_player_name_label = tk.Label(self.frame, text="BlackPlayer:",
                                        background="#FFFFFF",
                                        font=('Helvetica', MainWindow.TEXT_SIZE, 'bold'))
        black_player_name_label.grid(row=2, column=0, sticky="e")

        self.timer_label = tk.Label(self.frame, image=chess_clock_image_tk, background="#FFFFFF")
        self.timer_label.image = chess_clock_image_tk
        self.timer_label.grid(row=3, column=0, sticky="e", pady=MainWindow.PADY)

        self.combobox = ttk.Combobox(self.frame, values=["-", "1 min", "3 min", "5 min", "10 min", "15 min", "20 min", "25 min",
                                                    "30 min", "60 min", "90 min"], width=10, state="readonly")
        self.combobox.current(1)
        self.combobox.grid(row=3, column=1, sticky="w", padx=5, pady=MainWindow.PADY)

        # Bind the <Enter> and <Leave> events to the button
        self.start_button.bind("<Enter>", self.on_enter_startButton)
        self.start_button.bind("<Leave>", self.on_leave_startButton)

        # Bind the <Enter> and <Leave> events to the button
        self.exit_button.bind("<Enter>", self.on_enter_exitButton)
        self.exit_button.bind("<Leave>", self.on_leave_exitButton)

    def add_label(self, frame, text: str, row: int, col: int, colspan: int) -> tk.Label:
        label = tk.Label(frame, text=text,
                         background="#FFFFFF",
                         font=('Helvetica', MainWindow.TEXT_SIZE, 'bold'))
        label.grid(row=row, column=col, columnspan=colspan)
        return label

    def add_entry(self, frame, default_value, row: int, col: int) -> tk.Entry:
        entry = tk.Entry(frame)
        entry.insert(0, default_value)
        entry.grid(row=row, column=col, sticky="w", padx=5)
        return entry

    def add_button(self, frame, text: str, command: Callable, row: int, col: int,
                   colspan: int, width: int, height: int, color: str) -> tk.Button:
        button = tk.Button(frame,
                           text=text,
                           command=command,
                           background=color,
                           foreground='black',
                           font=('Helvetica', 16),
                           borderwidth=2,
                           relief="groove",
                           width= width,
                           height=height)
        button.grid(row=row, column=col, columnspan=colspan, pady=MainWindow.PADY)
        # button.config(width=width, height=height)
        return button

    def add_image_to_button(self, button, image_path: str):
        image = Image.open(image_path)
        image = image.resize((60, 60))
        image_tk = ImageTk.PhotoImage(image)
        button.config(image=image_tk,  width="270", height="80")
        button.image = image_tk

    def open_new_window(self):
        try:
            time: int = int(self.combobox.get().split(" ")[0]) * 60
        except ValueError:
            time = None
        game = Game("Chess Game", self.white_player_name.get(), self.black_player_name.get(), time=time)
        # game.run()

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



