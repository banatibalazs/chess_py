import tkinter as tk
from PIL import Image, ImageTk

from src.view.chess_gui_abs import ChessGuiAbs

WH_KNIGHT_IMAGE_PATH = "../../resources/images/pieces/wh_knight.png"
WH_BISHOP_IMAGE_PATH = "../../resources/images/pieces/wh_bishop.png"
WHITE_COLOR = "#ffffee"
BLACK_COLOR = "#5f915f"
REQUIRED_COLOR = "#cadbf1"


class ChessBoard(ChessGuiAbs):
    def __init__(self, rows=8, columns=8, color1=WHITE_COLOR, color2=BLACK_COLOR, square_size=100):
        super().__init__()
        """Constructor for ChessBoard."""
        self.rows = rows
        self.columns = columns
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}
        self.images = {}  # To keep reference to images

        self.toggle_color1 = "#ff0000"  # New color for squares originally of color1
        self.toggle_color2 = "#cc0000"  # New color for squares originally of color2

        self.geometry(f"{columns * 100}x{rows * 100}")
        self.square_size = square_size

        self.frame = tk.Frame(self)
        self.frame.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        self.canvas = tk.Canvas(self.frame, borderwidth=0, highlightthickness=0, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.bind("<Button-1>", self.on_square_clicked)
        self.canvas.bind("<Button-3>", self.toggle_square_color)  # Bind right-click event
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_drop)
        self.currently_dragged = None
        self.valid_coordinates = ((0, 0), (0, 1), (1, 0), (1, 1))

    def resize_image(self, image_path, factor):
        """Resize an image by a specified factor"""
        # Open the image file
        img = Image.open(image_path)
        # Calculate the new size
        width, height = img.size
        new_size = (int(width * factor), int(height * factor))
        # Resize the image
        img_resized = img.resize(new_size, Image.LANCZOS)
        # Convert the PIL image to a PhotoImage
        photo_img = ImageTk.PhotoImage(img_resized)
        return photo_img

    def add_piece(self, name, image_path, row=0, column=0):
        """Add a piece to the playing board"""
        image = self.resize_image(image_path, 0.8)
        self.canvas.create_image(0, 0, image=image, tags=(name, "piece"), anchor="c")
        self.pieces[name] = (row, column)
        self.images[name] = image  # To keep a reference to the image

    def toggle_square_color(self, event):
        """Handle right-click event to toggle square color"""
        col = event.x // self.square_size
        row = event.y // self.square_size

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
        self.square_size = min(event.width // self.columns, event.height // self.rows)
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.square_size)
                y1 = ((7 - row) * self.square_size)
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2

        # Redraw the pieces after the board
        for name in self.pieces:
            x0, y0 = self.pieces[name]
            self.canvas.coords(name, (y0 * self.square_size) + self.square_size / 2, ((7 - x0) * self.square_size) + self.square_size / 2)
            self.canvas.tag_raise(name)

    def on_square_clicked(self, event):
        """Handle square click event"""
        col = event.x // self.square_size
        row = event.y // self.square_size
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
            nearest_col = round((x - self.square_size / 2) / self.square_size)
            nearest_row = 7 - round((y - self.square_size / 2) / self.square_size)
            # Check if the new coordinates are within the board boundaries
            if 0 <= nearest_col < self.columns and 0 <= nearest_row < self.rows:
                self.canvas.coords(self.currently_dragged, x, y)

    def on_drop(self, event):
        """Handle drop event"""
        if self.currently_dragged is not None:  # Only drop the currently dragged piece
            x, y = event.x, event.y
            # Calculate the nearest square to the drop location
            nearest_col = round((x - self.square_size / 2) / self.square_size)
            nearest_row = 7 - round((y - self.square_size / 2) / self.square_size)
            # Check if the new coordinates are within the board boundaries
            if 0 <= nearest_col < self.columns and 0 <= nearest_row < self.rows:
                # Check if the square has the required color or coordinate
                if (nearest_row, nearest_col) in self.valid_coordinates:
                    print(f"Piece {self.currently_dragged} dropped at ({nearest_row}, {nearest_col})")
                    # Move the piece to the new location
                    self.pieces[self.currently_dragged] = (nearest_row, nearest_col)
                    self.canvas.coords(self.currently_dragged, (nearest_col * self.square_size) + self.square_size / 2,
                                       ((7 - nearest_row) * self.square_size) + self.square_size / 2)
                else:
                    # The square doesn't have the required color or coordinate, move the piece back to its original location
                    original_row, original_col = self.pieces[self.currently_dragged]
                    self.canvas.coords(self.currently_dragged, (original_col * self.square_size) + self.square_size / 2,
                                       ((7 - original_row) * self.square_size) + self.square_size / 2)
            self.currently_dragged = None  # Reset the currently dragged piece

    def move_piece(self, name, row, col):
        """Move a piece to a specified location"""
        if name in self.pieces:
            # Calculate the coordinates of the center of the destination square
            x = (col * self.square_size) + self.square_size / 2
            y = (row * self.square_size) + self.square_size / 2
            # Move the piece to the destination square
            self.canvas.coords(name, x, y)
            # Update the position of the piece
            self.pieces[name] = (row, col)

    def update_square_color(self, color, row, col):
        """Update the color of a specific square"""
        # Calculate the coordinates of the square
        # x1 = (col * self.square_size)
        # y1 = ((7 - row) * self.square_size)
        # x2 = x1 + self.square_size
        # y2 = y1 + self.square_size
        # # Find the square
        # square = self.canvas.find_overlapping(x1, y1, x2, y2)
        # # Update the color of the square
        # for item in square:
        #     if "square" in self.canvas.gettags(item):
        #         self.canvas.itemconfig(item, fill=color)
        pass

    def update_timer_label(self, time, color):
        pass

    def update_labels(self, white_player_score, black_player_score, snapshot_number, total_snapshot_number):
        pass

    def update_square_image(self, image_path, row, col):
        # """Update the image of a piece at a specific square"""
        # Calculate the coordinates of the square
        # x = (col * self.square_size) + self.square_size / 2
        # y = ((7 - row) * self.square_size) + self.square_size / 2
        # Find the piece at the square
        # piece = self.canvas.find_closest(x, y)
        # if piece:
            # If there is a piece at the square, delete it
            # self.canvas.delete(piece[0])
        # Resize the new image
        # image = self.resize_image(WH_BISHOP_IMAGE_PATH, 0.8)
        # # Add the new image to the square
        # self.canvas.create_image(x, y, image=image, tags=("piece",), anchor="c")
        # # Keep a reference to the image
        # self.images[(row, col)] = image
        self.add_piece("player1", image_path, row, col)



if __name__ == "__main__":
    # root = tk.Tk()
    board = ChessBoard()
    # board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    player1 = WH_BISHOP_IMAGE_PATH
    player2 = WH_KNIGHT_IMAGE_PATH
    board.add_piece("player1", player1, 0, 0)
    board.add_piece("player2", player2, 0, 1)
    board.add_piece("player3", player1, 0, 2)
    board.add_piece("player4", player2, 0, 3)


    # board.update_square_image(WH_KNIGHT_IMAGE_PATH, 1, 1)
    # board.update_square_image(WH_KNIGHT_IMAGE_PATH, 1, 2)
    # board.update_square_image(WH_KNIGHT_IMAGE_PATH, 1, 3)
    board.mainloop()
    board.move_piece("player1", 1, 1)
