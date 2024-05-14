import tkinter as tk
from PIL import Image, ImageTk

#
# class Square(tk.Button):
#     def __init__(self, parent, **kwargs):
#         self.row = kwargs.pop('row', None)
#         self.col = kwargs.pop('col', None)
#         self.onclick = kwargs.pop('onclick', None)
#         self.on_right_click = kwargs.pop('onrightclick', None)  # New parameter for right click event
#         tk.Button.__init__(self, parent, kwargs, command=self.click)
#         self.bind("<Button-3>", self.right_click)  # Bind right click event to the new method
#
#     def click(self):
#         if self.onclick:
#             self.onclick(self.row, self.col)
#
#     def right_click(self, event):  # New method for handling right click event
#         if self.on_right_click:
#             self.on_right_click(self.row, self.col)
#
#     def set_image(self, piece_image_path):
#         piece_image = Image.open(piece_image_path)
#         piece_image = piece_image.resize((105, 110))
#         piece_image_tk = ImageTk.PhotoImage(piece_image)  # Use ImageTk.PhotoImage here
#         self.image = piece_image_tk
#         self.config(image=piece_image_tk, width="80", height="80")
#         # self.show_image_in_new_window(piece_image_path)
#

class Square(tk.Button):
    def __init__(self, master=None, onclick=None, row=0, col=0, **kw):
        super().__init__(master, command=lambda: onclick(row, col), **kw)
        self.row = row
        self.col = col
        self.image_path = None
        self.image = None

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
