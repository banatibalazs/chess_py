import tkinter as tk

class Square(tk.Button):
    def __init__(self, master=None, onclick=None, x=0, y=0, **kw):
        super().__init__(master, command=lambda: onclick(x, y), **kw)
        self.x = x
        self.y = y