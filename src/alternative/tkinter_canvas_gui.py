# import os
# import threading
# import tkinter as tk
# from PIL import Image, ImageTk
#
# from src.view.chess_gui_abs import ChessGuiAbs
#
#
# # Get the directory containing the current script
# script_dir = os.path.dirname(os.path.realpath(__file__))
# print("Script dir:  ",script_dir)
# WH_BISHOP_IMAGE_PATH = os.path.join(script_dir, "bl_bishop.png")
#
# print("White bishop path: ",WH_BISHOP_IMAGE_PATH)
# WHITE_COLOR = "#ffffee"
# BLACK_COLOR = "#5f915f"
# REQUIRED_COLOR = "#cadbf1"
#
#
# class ChessBoard(ChessGuiAbs):
#     def __init__(self, game,
#                  rows=8, columns=8, color1=WHITE_COLOR, color2=BLACK_COLOR, square_size=100):
#         tk.Toplevel.__init__(self)
#         # self.click_on_board = click_on_board
#         # self.right_button_click = right_button_click
#         # self.left_button_click = left_button_click
#         self.game = game
#
#         """Constructor for ChessBoard."""
#         self.rows = rows
#         self.columns = columns
#         self.color1 = color1
#         self.color2 = color2
#         self.pieces = {}
#         self.images = {}  # To keep reference to images
#
#         self.toggle_color1 = "#ff0000"  # New color for squares originally of color1
#         self.toggle_color2 = "#cc0000"  # New color for squares originally of color2
#
#         self.geometry(f"{columns * 100}x{rows * 100}")
#         self.square_size = square_size
#
#         self.frame = tk.Frame(self)
#         self.frame.pack(side="top", fill="both", expand=True, padx=2, pady=2)
#
#         self.canvas = tk.Canvas(self.frame, borderwidth=0, highlightthickness=0, background="bisque")
#         self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
#
#         self.click_thread = None
#         self.canvas.bind("<Button-1>", self.on_square_clicked)
#         self.canvas.bind("<Button-3>", self.toggle_square_color)  # Bind right-click event
#         self.canvas.bind("<B1-Motion>", self.on_drag)
#         self.canvas.bind("<ButtonRelease-1>", self.on_drop)
#         self.currently_dragged = None
#         self.valid_coordinates = ((0, 0), (0, 1), (1, 0), (1, 1))
#         self.refresh()
#
#     def resize_image(self, image_path, factor):
#         """Resize an image by a specified factor"""
#         # Open the image file
#         img = Image.open(image_path)
#         # Calculate the new size
#         width, height = img.size
#         new_size = (int(width * factor), int(height * factor))
#         # Resize the image
#         img_resized = img.resize(new_size, Image.LANCZOS)
#         # Convert the PIL image to a PhotoImage
#         photo_img = ImageTk.PhotoImage(img_resized)
#         return photo_img
#
#     def toggle_square_color(self, event):
#         """Handle right-click event to toggle square color"""
#         col = event.x // self.square_size
#         row = event.y // self.square_size
#
#         # Get the item that was clicked
#         item_id = self.canvas.find_closest(event.x, event.y)[0]
#         tags = self.canvas.gettags(item_id)
#
#         # If the item is a piece, get the ID of the square below it
#         if "piece" in tags:
#             square_id = [id for id in self.canvas.find_overlapping(*self.canvas.bbox(item_id)) if id != item_id][0]
#         else:
#             square_id = item_id
#
#         current_color = self.canvas.itemcget(square_id, "fill")
#         print(f"Square at ({row}, {col}) clicked! Color: {current_color}")
#
#         if (row + col) % 2 == 1:
#             print("White square")
#             if current_color == WHITE_COLOR:
#                 new_color = self.toggle_color1
#             else:
#                 new_color = WHITE_COLOR
#         else:
#             print("Black square")
#             if current_color == BLACK_COLOR:
#                 new_color = self.toggle_color2
#             else:
#                 new_color = BLACK_COLOR
#
#         self.canvas.itemconfig(square_id, fill=new_color)
#
#     def refresh(self, event={}):
#         """Redraw the board"""
#         self.canvas.delete("square")
#         color = self.color2
#         # self.square_size = min(event.width // self.columns, event.height // self.rows)
#         for row in range(self.rows):
#             color = self.color1 if color == self.color2 else self.color2
#             for col in range(self.columns):
#                 x1 = (col * self.square_size)
#                 y1 = ((7 - row) * self.square_size)
#                 x2 = x1 + self.square_size
#                 y2 = y1 + self.square_size
#                 self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
#                 color = self.color1 if color == self.color2 else self.color2
#
#         # Redraw the pieces after the board
#         for name in self.pieces:
#             x0, y0 = self.pieces[name]
#             self.canvas.coords(name, (y0 * self.square_size) + self.square_size / 2, ((7 - x0) * self.square_size) + self.square_size / 2)
#             self.canvas.tag_raise(name)
#
#     # def on_square_clicked(self, event):
#     #     col = event.x // self.square_size
#     #     row = event.y // self.square_size
#     #     print("Square click at: ", row, col)
#     #
#     #     if self.currently_dragged is None:
#     #         # If no piece is being dragged, handle the click as a move
#     #         self.game.click_on_board(row, col)
#     #     else:
#     #         # If a piece is being dragged, handle the click as the start of a drag
#     #         self.handle_click_on_square(event)
#
#     def on_square_clicked(self, event):
#         col = event.x // self.square_size
#         row = event.y // self.square_size
#         print("Square click at: ", row, col)
#
#         if self.click_thread is None:
#             print("Starting thread to call click_on_board")
#             self.click_thread = threading.Thread(target=self.game.click_on_board, args=(row, col))
#             print("Thread started")
#             self.click_thread.start()
#
#         # Check if a piece is clicked
#         for name in self.pieces:
#             if self.canvas.bbox(name):
#                 x1, y1, x2, y2 = self.canvas.bbox(name)
#                 if (x1 < event.x < x2) and (y1 < event.y < y2):
#                     self.currently_dragged = name  # Set the currently dragged piece
#                     self.canvas.tag_raise(name)  # Bring the piece to the top
#                     return
#
#     def on_drag(self, event):
#         """Handle drag event"""
#         if self.currently_dragged is not None:  # Only move the currently dragged piece
#             x, y = event.x, event.y
#             self.canvas.coords(self.currently_dragged, x, y)
#
#     def on_drop(self, event):
#         """Handle drop event"""
#         if self.currently_dragged is not None:  # Only drop the currently dragged piece
#             x, y = event.x, event.y
#             # Calculate the nearest square to the drop location
#             nearest_col = round((x - self.square_size / 2) / self.square_size)
#             nearest_row = 7 - round((y - self.square_size / 2) / self.square_size)
#             # Check if the new coordinates are within the board boundaries
#             if 0 <= nearest_col < self.columns and 0 <= nearest_row < self.rows:
#                 # Move the piece to the new location
#                 self.pieces[self.currently_dragged] = (nearest_row, nearest_col)
#                 self.canvas.coords(self.currently_dragged, (nearest_col * self.square_size) + self.square_size / 2,
#                                    ((7 - nearest_row) * self.square_size) + self.square_size / 2)
#             else:
#                 # The square doesn't have the required color or coordinate, move the piece back to its original location
#                 original_row, original_col = self.pieces[self.currently_dragged]
#                 self.canvas.coords(self.currently_dragged, (original_col * self.square_size) + self.square_size / 2,
#                                    ((7 - original_row) * self.square_size) + self.square_size / 2)
#             self.currently_dragged = None  # Reset the currently dragged piece
#
#     def move_piece(self, name, row, col):
#         """Move a piece to a specified location"""
#         if name in self.pieces:
#             # Calculate the coordinates of the center of the destination square
#             x = (col * self.square_size) + self.square_size / 2
#             y = (7 - row * self.square_size) + self.square_size / 2
#             # Move the piece to the destination square
#             self.canvas.coords(name, x, y)
#             # Update the position of the piece
#             self.pieces[name] = (row, col)
#
#     def update_square_color(self, color, row, col):
#         """Update the color of a specific square"""
#         # Calculate the coordinates of the square
#         # x1 = (col * self.square_size)
#         # y1 = ((7 - row) * self.square_size)
#         # x2 = x1 + self.square_size
#         # y2 = y1 + self.square_size
#         # # Find the square
#         # square = self.canvas.find_overlapping(x1, y1, x2, y2)
#         # # Update the color of the square
#         # for item in square:
#         #     if "square" in self.canvas.gettags(item):
#         #         self.canvas.itemconfig(item, fill=color)
#         pass
#
#
#     def update_timer_label(self, time, color):
#         pass
#
#     def update_labels(self, white_player_score, black_player_score, snapshot_number, total_snapshot_number):
#         pass
#
#     def update_square_image(self, image_path, row, col):
#         """Update the image of a piece at a specific square"""
#         # Find the piece at the given square
#         self.add_piece(f"{row}-{col}", image_path, row, col)
#         # for name, (piece_row, piece_col) in self.pieces.items():
#         #     if piece_row == row and piece_col == col:
#         #         # Resize the new image
#         #         image = self.resize_image(image_path, 0.8)
#         #         # Update the image of the piece
#         #         self.canvas.itemconfig(name, image=image)
#         #         # Update the reference to the image
#         #         self.images[name] = image
#         #         break
#         # self.canvas.update()
#
#     def add_piece(self, name, image_path, row=0, column=0):
#         """Add a piece to the playing board"""
#         image = self.resize_image(image_path, 0.8)
#         self.pieces[name] = (row, column)
#         self.images[name] = image  # To keep a reference to the image
#         x = (column * self.square_size) + self.square_size / 2
#         y = ((7 - row) * self.square_size) + self.square_size / 2
#         self.canvas.create_image(x, y, image=image, tags=(name, "piece"), anchor="c")
