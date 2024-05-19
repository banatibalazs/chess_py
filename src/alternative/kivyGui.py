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

        self.toggle_color1 = "#ff0000"  # New color for squares originally of color1
        self.toggle_color2 = "#cc0000"  # New color for squares originally of color2

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.bind("<Button-1>", self.on_square_clicked)
        self.canvas.bind("<Button-3>", self.toggle_square_color)  # Bind right-click event
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_drop)
        self.currently_dragged = None

    def addpiece(self, name, image_path, row=0, column=0):
        """Add a piece to the playing board"""
        image = tk.PhotoImage(file=image_path)
        # Resize the image
        image = image.subsample(2, 2)  # Reduce the size by a factor of 2
        self.canvas.create_image(0, 0, image=image, tags=(name, "piece"), anchor="c")
        self.pieces[name] = (row, column)
        self.images[name] = image  # To keep a reference to the image

    def toggle_square_color(self, event):
        """Handle right-click event to toggle square color"""
        col = event.x // self.size
        row = event.y // self.size

        item_id = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item_id)

        # If the item is a piece, ignore the click
        if "piece" in tags:
            return

        current_color = self.canvas.itemcget(item_id, "fill")
        print(f"Square at ({row}, {col}) clicked! Color: {current_color}")

        if (row + col) % 2 == 1:
            print("White square")
            if current_color == WHITE_COLOR:
                new_color = self.toggle_color1
            else:
                new_color = WHITE_COLOR
        else:
            print("Black square")
            if current_color == BLACK_COLOR:
                new_color = self.toggle_color2
            else:
                new_color = BLACK_COLOR

        self.canvas.itemconfig(item_id, fill=new_color)

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
        x, y = event.x, event.y
        for name in self.pieces:
            if self.canvas.bbox(name):
                x1, y1, x2, y2 = self.canvas.bbox(name)
                if (x1 < x < x2) and (y1 < y < y2):
                    self.currently_dragged = name  # Set the currently dragged piece

    def on_drag(self, event):
        """Handle drag event"""
        if self.currently_dragged is not None:  # Only move the currently dragged piece
            x, y = event.x, event.y
            # Calculate the nearest square to the current location
            nearest_col = round((x - self.size / 2) / self.size)
            nearest_row = 7 - round((y - self.size / 2) / self.size)
            # Check if the new coordinates are within the board boundaries
            if 0 <= nearest_col < self.columns and 0 <= nearest_row < self.rows:
                self.canvas.coords(self.currently_dragged, x, y)

    def on_drop(self, event):
        """Handle drop event"""
        if self.currently_dragged is not None:  # Only drop the currently dragged piece
            x, y = event.x, event.y
            # Calculate the nearest square to the drop location
            nearest_col = round((x - self.size / 2) / self.size)
            nearest_row = 7 - round((y - self.size / 2) / self.size)
            # Check if the new coordinates are within the board boundaries
            if 0 <= nearest_col < self.columns and 0 <= nearest_row < self.rows:
                # Snap the piece to the nearest square
                self.pieces[self.currently_dragged] = (nearest_row, nearest_col)
                self.canvas.coords(self.currently_dragged, (nearest_col * self.size) + self.size / 2,
                                   ((7 - nearest_row) * self.size) + self.size / 2)
            self.currently_dragged = None  # Reset the currently dragged piece

    def move_piece(self, name, row, col):
        """Move a piece to a specified location"""
        if name in self.pieces:
            # Calculate the coordinates of the center of the destination square
            x = (col * self.size) + self.size / 2
            y = ((7 - row) * self.size) + self.size / 2
            # Move the piece to the destination square
            self.canvas.coords(name, x, y)
            # Update the position of the piece
            self.pieces[name] = (row, col)

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
    board.move_piece("player1", 1, 1)
