import tkinter as tk
from PIL import Image, ImageTk

class Square(tk.Button):
    def __init__(self, master=None, onclick=None, x=0, y=0, **kw):
        super().__init__(master, command=lambda: onclick(x, y), **kw)
        self.x = x
        self.y = y
        self.image_path = None

    def set_image(self, piece_image_path):
        piece_image = Image.open(piece_image_path)
        piece_image = piece_image.resize((105, 110))
        piece_image_tk = ImageTk.PhotoImage(piece_image)  # Use ImageTk.PhotoImage here
        self.image = piece_image_tk
        self.config(image=piece_image_tk, width="80", height="80")
        # self.show_image_in_new_window(piece_image_path)

    def set_color(self, color):
        self.config(bg=color)

    def get_image_path(self):
        return self.image_path

