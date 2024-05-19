import tkinter as tk
from tkinter import PhotoImage

WH_KNIGHT_IMAGE_PATH = "../../resources/images/pieces/wh_knight.png"
WH_BISHOP_IMAGE_PATH = "../../resources/images/pieces/wh_bishop.png"
WHITE_COLOR = "#ffffee"
BLACK_COLOR = "#5f915f"

class ChessBoard(tk.Frame):
    def __init__(self, parent, rows=8, columns=8, size=100, color1=WHITE_COLOR, color2=BLACK_COLOR):
        """Constructor for ChessBoard."""
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}
        self.images = {}  # To keep reference to images

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.bind("<Button-1>", self.on_square_clicked)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_drop)

    def addpiece(self, name, image_path, row=0, column=0):
        """Add a piece to the playing board"""
        image = tk.PhotoImage(file=image_path)
        # Resize the image
        image = image.subsample(2, 2)  # Reduce the size by a factor of 2
        self.canvas.create_image(0, 0, image=image, tags=(name, "piece"), anchor="c")
        self.pieces[name] = (row, column)
        self.images[name] = image  # To keep a reference to the image

    # def addpiece(self, name, image, row=0, column=0):
    #     """Add a piece to the playing board"""
    #     self.canvas.create_image(0, 0, image=image, tags=(name, "piece"), anchor="c")
    #     self.pieces[name] = (row, column)
    #     self.images[name] = image

    def refresh(self, event={}):
        """Redraw the board"""
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = ((7 - row) * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2

        # Redraw the pieces after the board
        for name in self.pieces:
            x0, y0 = self.pieces[name]
            self.canvas.coords(name, (y0 * self.size) + self.size / 2, ((7 - x0) * self.size) + self.size / 2)
            self.canvas.tag_raise(name)

    def on_square_clicked(self, event):
        """Handle square click event"""
        col = event.x // self.size
        row = event.y // self.size
        print(f"Square at ({row}, {col}) clicked!")

    def on_drag(self, event):
        """Handle drag event"""
        x, y = event.x, event.y
        for name in self.pieces:
            if self.canvas.bbox(name):
                x1, y1, x2, y2 = self.canvas.bbox(name)
                if (x1 < x < x2) and (y1 < y < y2):
                    self.canvas.coords(name, x, y)

    def on_drop(self, event):
        """Handle drop event"""
        x, y = event.x, event.y
        for name in self.pieces:
            if self.canvas.bbox(name):
                x1, y1, x2, y2 = self.canvas.bbox(name)
                if (x1 < x < x2) and (y1 < y < y2):
                    # Calculate the nearest square to the drop location
                    nearest_col = round((x - self.size / 2) / self.size)
                    nearest_row = 7 - round((y - self.size / 2) / self.size)
                    # Snap the piece to the nearest square
                    self.pieces[name] = (nearest_row, nearest_col)
                    self.canvas.coords(name, (nearest_col * self.size) + self.size / 2,
                                       ((7 - nearest_row) * self.size) + self.size / 2)

if __name__ == "__main__":
    root = tk.Tk()
    board = ChessBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    # player1 = PhotoImage(file=WH_KNIGHT_IMAGE_PATH)  # replace with your images
    # player2 = PhotoImage(file=WH_BISHOP_IMAGE_PATH)  # replace with your images
    player1 = WH_BISHOP_IMAGE_PATH
    player2 = WH_KNIGHT_IMAGE_PATH
    board.addpiece("player1", player1, 0, 0)
    board.addpiece("player2", player2, 0, 1)
    root.mainloop()
