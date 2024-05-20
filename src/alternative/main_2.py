import multiprocessing
import threading
import time
from typing import Tuple, List, Optional, Dict

import numpy as np
import pygame

from src.alternative.game import Game

WH_KNIGHT_IMAGE_PATH = "../../resources/images/pieces/wh_knight.png"
WH_BISHOP_IMAGE_PATH = "../../resources/images/pieces/wh_bishop.png"
WH_ROOK_IMAGE_PATH = "../../resources/images/pieces/wh_rook.png"
WH_QUEEN_IMAGE_PATH = "../../resources/images/pieces/wh_queen.png"
WH_KING_IMAGE_PATH = "../../resources/images/pieces/wh_king.png"
WH_PAWN_IMAGE_PATH = "../../resources/images/pieces/wh_pawn.png"

EMPTY_SQUARE_IMAGE_PATH = "../../resources/images/welcome_page/empty.png"

BL_KNIGHT_IMAGE_PATH = "../../resources/images/pieces/bl_knight.png"
BL_BISHOP_IMAGE_PATH = "../../resources/images/pieces/bl_bishop.png"
BL_ROOK_IMAGE_PATH = "../../resources/images/pieces/bl_rook.png"
BL_QUEEN_IMAGE_PATH = "../../resources/images/pieces/bl_queen.png"
BL_KING_IMAGE_PATH = "../../resources/images/pieces/bl_king.png"
BL_PAWN_IMAGE_PATH = "../../resources/images/pieces/bl_pawn.png"

POSSIBLE_FIELDS_COLOR_DARK = (144, 169, 245)
POSSIBLE_FIELDS_COLOR_LIGHT = (202, 219, 241)
BLACK_SQUARE_COLOR = (95, 145, 95)
WHITE_SQUARE_COLOR = (255, 255, 238)
SELECTED_SQUARE_COLOR_LIGHT = (200, 100, 100)
SELECTED_SQUARE_COLOR_DARK = (200, 0, 0)



class ChessGUI:
    def __init__(self, screen_width=800, screen_height=800):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Chess Game")
        self.square_size = screen_width // 8  # Assuming board is 8x8
        self.running = True
        self.board_surface = pygame.Surface((screen_width, screen_height))
        self.colors = [[WHITE_SQUARE_COLOR if (row + col) % 2 == 0 else BLACK_SQUARE_COLOR for col in range(8)] for row in range(8)]  # Light and dark square colors
        self.original_colors = [WHITE_SQUARE_COLOR, BLACK_SQUARE_COLOR]
        self.dragging = False  # Indicates whether we're currently dragging an object
        self.dragged_object_pos = None  # The object that is being dragged
        self.image_size = (self.square_size, self.square_size)  # Define the standard image size
        self.images_pos = [[col * self.square_size, 0] for col in range(8)]  # The positions of the images
        self.board = [[None for _ in range(8)] for _ in range(8)]  # Initialize the board with None
        self.game = Game()
        self.possible_fields = []
        self.selected_piece_pos = None
        self._byte_to_piece_image_path: Dict[np.byte, str] = {
            np.byte(-6): BL_KING_IMAGE_PATH,
            np.byte(-5): BL_QUEEN_IMAGE_PATH,
            np.byte(-4): BL_BISHOP_IMAGE_PATH,
            np.byte(-3): BL_KNIGHT_IMAGE_PATH,
            np.byte(-2): BL_ROOK_IMAGE_PATH,
            np.byte(-1): BL_PAWN_IMAGE_PATH,

            np.byte(0): EMPTY_SQUARE_IMAGE_PATH,

            np.byte(6): WH_KING_IMAGE_PATH,
            np.byte(5): WH_QUEEN_IMAGE_PATH,
            np.byte(4): WH_BISHOP_IMAGE_PATH,
            np.byte(3): WH_KNIGHT_IMAGE_PATH,
            np.byte(2): WH_ROOK_IMAGE_PATH,
            np.byte(1): WH_PAWN_IMAGE_PATH
        }
        self.init_images()

    def set_image(self, row: int, col: int, image_path: str = EMPTY_SQUARE_IMAGE_PATH):
        image = pygame.image.load(image_path)  # Load the image
        image = pygame.transform.scale(image, (self.square_size, self.square_size))  # Scale the image to fit the square
        self.board[row][col] = image  # Store the image at the specified row and column

    def init_images(self):
        piece_board = self.game.get_piece_board()
        for row in range(8):
            for col in range(8):
                image = pygame.image.load(self._byte_to_piece_image_path[piece_board[row][col]])  # Load the image
                image = pygame.transform.scale(image, (self.square_size, self.square_size))  # Scale the image to fit the square
                self.board[row][col] = image

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(self.board_surface, self.colors[row][col],
                                 pygame.Rect(col * self.square_size, row * self.square_size, self.square_size,
                                             self.square_size))
                # If there's an image at this square, draw it
                if self.board[row][col] is not None:
                    self.board_surface.blit(self.board[row][col], (col * self.square_size, row * self.square_size))
        pygame.display.flip()

    def game_loop(self):
        # Create a clock object
        clock = pygame.time.Clock()

        # Create a font object
        font = pygame.font.Font(None, 30)
        while self.running:

            # Cap the frame rate to 60 FPS
            clock.tick(60)
            # Get the current FPS
            fps = clock.get_fps()
            # Render the FPS on a surface
            fps_surface = font.render(f"FPS: {fps:.2f}", True, pygame.Color('red'))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Check if the left mouse button was pressed
                        # Start dragging
                        self.dragged_object_pos = self.get_object_at_pos(event.pos)
                        self.dragged_object = self.board[event.pos[1] // self.square_size][event.pos[0] // self.square_size]
                        if self.dragged_object_pos is not None:  # Check if an image was clicked
                            self.dragging = True
                            self.original_pos = self.dragged_object_pos.copy()  # Store the original position
                            # Store the original square coordinates
                            self.original_square = (
                                self.dragged_object_pos[0] // self.square_size, self.dragged_object_pos[1] // self.square_size)
                            # Change the color of the square that the image was on
                            self.left_button_clicked(event)
                            # Remove the image from the original square
                            self.board[self.original_square[1]][self.original_square[0]] = None

                    elif event.button == 2:  # Check if the middle mouse button was pressed
                        self.dragged_object_pos = self.get_object_at_pos(event.pos)
                        if self.dragged_object_pos is not None:
                            # start_square = (self.dragged_object_pos[0] // self.square_size,
                            #                 self.dragged_object_pos[1] // self.square_size)
                            start_square = self.get_square_position(self.dragged_object_pos)
                            # end_square = (4, 4)  # Replace with the actual end square
                            self.make_move(start_square)

                    elif event.button == 3:  # Check if the right mouse button was pressed
                        square = (event.pos[0] // self.square_size, event.pos[1] // self.square_size)
                        self.right_button_clicked(square)

                elif event.type == pygame.MOUSEMOTION:
                    # If we're dragging an object, update its position to follow the mouse
                    if self.dragging and self.dragged_object_pos is not None:
                        new_x = event.pos[0] - self.square_size // 2
                        new_y = event.pos[1] - self.square_size // 2
                        # Check if the new position is within the board
                        if 0 <= new_x + self.square_size // 2 < 8 * self.square_size and 0 <= new_y + self.square_size // 2 < 8 * self.square_size:
                            self.dragged_object_pos[0] = new_x
                            self.dragged_object_pos[1] = new_y

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Check if the left mouse button was released
                        if self.dragged_object_pos is not None:  # Check if an image was being dragged
                            square_x, square_y = self.get_square_position(self.dragged_object_pos)
                            if 0 <= square_x < 8 and 0 <= square_y < 8:
                                # Set the image at the new square
                                if self.original_pos != self.dragged_object_pos and \
                                        (square_y, square_x) in self.possible_fields:
                                    self.board[square_y][square_x] = self.dragged_object
                                    self.game.click_on_board(event.pos[1] // self.square_size, event.pos[0] // self.square_size)
                                else:
                                    self.board[self.original_square[1]][self.original_square[0]] = self.dragged_object
                                self.change_square_color(self.original_square[1], self.original_square[0],
                                                         self.original_colors[(self.original_square[1] +
                                                                               self.original_square[0]) % 2])
                                self.reset_possible_fields()
                                # Change the color of the original square back to its original color

                            self.dragged_object_pos = None

                        self.dragging = False

                self.draw_board()
                # Draw the board surface onto the screen
                self.screen.blit(self.board_surface, (0, 0))
                # If an image is being dragged, draw it at its current position
                if self.dragging and self.dragged_object is not None:
                    self.screen.blit(self.dragged_object, tuple(self.dragged_object_pos))

                # Blit the FPS surface onto the screen at position (10, 10)
                self.screen.blit(fps_surface, (10, 10))

                pygame.display.flip()

    def get_square_position(self, pos):
        square_x = (pos[0] + self.square_size // 2) // self.square_size
        square_y = (pos[1] + self.square_size // 2) // self.square_size
        return square_x, square_y

    def reset_possible_fields(self):
        if self.possible_fields is None:
            return
        for field in self.possible_fields:
            row, col = field
            self.change_square_color(row, col, self.original_colors[(row + col) % 2])
        self.possible_fields = []

    def get_object_at_pos(self, pos) -> Optional[List[int]]:
        for row in range(8):
            for col in range(8):
                if self.board[row][col] is not None:  # If there's an image at this square
                    image_pos = [col * self.square_size, row * self.square_size]
                    # Check if the mouse is over the image
                    if pygame.Rect(*image_pos, self.square_size, self.square_size).collidepoint(pos):
                        # print("Image selected for dragging")
                        return image_pos
        return None

    def right_button_clicked(self, square):
        image_path = '../../resources/images/pieces/pig.png'  # Replace with your actual image file path
        self.set_image(square[1], square[0], image_path)

    def left_button_clicked(self, event):
        print(f"Left button clicked at {event.pos}")
        row, col = event.pos[1] // self.square_size, event.pos[0] // self.square_size
        self.colors[row][col] = self.original_colors[(row + col) % 2]
        if self.selected_piece_pos != (row, col):
            self.game.click_on_board(row, col)
            self.selected_piece_pos = (row, col)

        if self.board[row][col] is not None:
            self.set_selected_piece_color(row, col)

        self.reset_possible_fields()
        selected_piece = self.game.get_selected_piece()
        if selected_piece is None:
            return
        self.possible_fields = selected_piece.possible_fields
        print(f" Possible fields: {self.possible_fields}")
        if self.possible_fields is not None:
            for field in self.possible_fields:
                row, col = field
                if (row + col) % 2 == 0:
                    color = POSSIBLE_FIELDS_COLOR_LIGHT
                else:
                    color = POSSIBLE_FIELDS_COLOR_DARK
                self.change_square_color(row, col, color)

    def set_selected_piece_color(self, row, col):
        if self.colors[row][col] == SELECTED_SQUARE_COLOR_LIGHT or self.colors[row][col] == SELECTED_SQUARE_COLOR_DARK:
            color = self.original_colors[(row + col) % 2]
        else:
            color = SELECTED_SQUARE_COLOR_LIGHT if (row + col) % 2 == 0 else SELECTED_SQUARE_COLOR_DARK
        self.colors[row][col] = color

    def reset_selected_piece_color(self, row, col):
        self.change_square_color(row, col, self.original_colors[(row + col) % 2])

    def reset_square_colors(self):
        for row in range(8):
            for col in range(8):
                self.change_square_color(row, col, self.original_colors[(row + col) % 2])

    def change_square_color(self, row, col, new_color: Tuple[int, int, int]):
        # print(f"Changing color of square ({row}, {col}) to {new_color}")
        self.colors[row][col] = new_color
        self.draw_board()

    def make_move(self, start_square, end_square=(4, 4)):
        # Get the image at the start square
        dragged_object = self.board[start_square[1]][start_square[0]]
        if dragged_object is None:
            # print(f"No image at square {start_square}")
            return

        distance = ((end_square[0] - start_square[0]) ** 2 + (end_square[1] - start_square[1]) ** 2) ** 0.5
        print(f"Moving image from {start_square} to {end_square} in {distance} steps")

        # Calculate the distance to move in each step
        dx = (end_square[0] - start_square[0]) * self.square_size / 10.0
        dy = (end_square[1] - start_square[1]) * self.square_size / 10.0

        # Remove the image from the start square
        self.board[start_square[1]][start_square[0]] = None

        # Move the image in small steps
        for i in range(10):
            # Update the position of the image
            self.dragged_object_pos = [start_square[0] * self.square_size + i * dx,
                                       start_square[1] * self.square_size + i * dy]
            # Redraw the board and the image
            self.screen.blit(dragged_object, tuple(map(int, self.dragged_object_pos)))
            self.draw_board()
            pygame.display.flip()

            # Draw the board surface onto the screen
            self.screen.blit(self.board_surface, (0, 0))

        # # Place the image on the end square
        self.board[end_square[1]][end_square[0]] = dragged_object


if __name__ == "__main__":
    gui = ChessGUI()
    gui.game_loop()
    print("Game over!")
