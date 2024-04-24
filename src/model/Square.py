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
        piece_image = piece_image.resize((150, 150))
        piece_image_tk = ImageTk.PhotoImage(piece_image)  # Use ImageTk.PhotoImage here
        self.image = piece_image_tk
        self.config(image=piece_image_tk, width="100", height="100")
        # self.show_image_in_new_window(piece_image_path)

    def get_image_path(self):
        return self.image_path

    def show_image_in_new_window( self ,image_path):
        # Create a new tkinter window
        new_window = tk.Toplevel()

        # Load the image
        image = Image.open(image_path)

        # Convert the PIL Image object to a PhotoImage object
        photo = ImageTk.PhotoImage(image)

        # Create a label and set its image option to the PhotoImage object
        label = tk.Label(new_window, image=photo)

        # Keep a reference to the image object to prevent it from being garbage collected
        label.image = photo

        # Add the label to the window
        label.pack()

