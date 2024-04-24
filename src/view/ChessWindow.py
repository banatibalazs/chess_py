import tkinter as tk

from src.controller.ClickController import ClickController
from src.model.Square import Square


class ChessWindow:
    def __init__(self, title):
        self.title = title
        self.root = tk.Tk()
        self.root.title(self.title)
        self.setup_ui()
        self.ClickController = ClickController()

    def setup_ui(self):
        # Create a 2D list to hold the button objects
        self.squares = []

        for i in range(8):
            row = []
            for j in range(8):
                # Create a button for each square
                square = Square(self.root, width=6, height=3, onclick=self.onclick, x=i, y=j,)
                square.grid(row=i, column=j, sticky="nsew")

                # Alternate the button color to create a checker pattern
                if (i + j) % 2 == 0:
                    square.config(bg='white')
                else:
                    square.config(bg='black')

                row.append(square)
            self.squares.append(row)

    def onclick(self, x, y):
        self.ClickController.click(x, y)

    def run(self):
        self.root.mainloop()
