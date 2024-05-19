import time
from typing import Tuple, List, Optional

import pygame


class ChessGUI:
    def __init__(self, screen_width=800, screen_height=800):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Chess Game")
        self.square_size = screen_width // 8  # Assuming board is 8x8
        self.running = True
        self.board_surface = pygame.Surface((screen_width, screen_height))
        self.colors = [[(233, 236, 239) if (row + col) % 2 == 0 else (125, 135, 150) for col in range(8)] for row in range(8)]  # Light and dark square colors
        self.original_colors = [(233, 236, 239), (125, 135, 150)]
        self.dragging = False  # Indicates whether we're currently dragging an object
        self.dragged_object_pos = None  # The object that is being dragged
        self.image_size = (self.square_size, self.square_size)  # Define the standard image size
        self.images_pos = [[col * self.square_size, 0] for col in range(8)]  # The positions of the images
        self.board = [[None for _ in range(8)] for _ in range(8)]  # Initialize the board with None

    def set_image(self, row: int, col: int, image_path: str = '../resources/images/pieces/wh_king.png'):
        image = pygame.image.load(image_path)  # Load the image
        image = pygame.transform.scale(image, (self.square_size, self.square_size))  # Scale the image to fit the square
        self.board[row][col] = image  # Store the image at the specified row and column

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
        while self.running:
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
                            self.left_button_clicked(self.original_square, event.pos)
                            # Remove the image from the original square
                            self.board[self.original_square[1]][self.original_square[0]] = None

                    elif event.button == 2:  # Check if the middle mouse button was pressed
                        self.dragged_object_pos = self.get_object_at_pos(event.pos)
                        if self.dragged_object_pos is not None:
                            start_square = (self.dragged_object_pos[0] // self.square_size,
                                            self.dragged_object_pos[1] // self.square_size)
                            # end_square = (4, 4)  # Replace with the actual end square
                            self.make_move(start_square)

                    elif event.button == 3:  # Check if the right mouse button was pressed
                        square = (event.pos[0] // self.square_size, event.pos[1] // self.square_size)
                        self.right_button_clicked(square, event.pos)

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
                        # Stop dragging
                        self.dragging = False
                        if self.dragged_object_pos is not None:  # Check if an image was being dragged
                            # Snap the image to the center of the square it is above
                            square_x = (self.dragged_object_pos[0] + self.square_size // 2) // self.square_size
                            square_y = (self.dragged_object_pos[1] + self.square_size // 2) // self.square_size
                            # Check if the new position is within the board
                            if 0 <= square_x < 8 and 0 <= square_y < 8:
                                self.dragged_object_pos[0] = square_x * self.square_size + self.square_size // 2 - \
                                                             self.image_size[0] // 2
                                self.dragged_object_pos[1] = square_y * self.square_size + self.square_size // 2 - \
                                                             self.image_size[0] // 2
                                # Set the image at the new square
                                self.board[square_y][square_x] = self.dragged_object
                            else:
                                # If the new position is not within the board, reset the position of the image to its original position
                                self.dragged_object_pos = self.original_pos
                            # Change the color of the original square back to its original color
                            self.change_square_color(self.original_square[1], self.original_square[0],
                                                     self.original_colors[(self.original_square[1] +
                                                         self.original_square[0]) % 2])
                            self.dragged_object_pos = None

                self.draw_board()
                # Draw the board surface onto the screen
                self.screen.blit(self.board_surface, (0, 0))
                # If an image is being dragged, draw it at its current position
                if self.dragging and self.dragged_object is not None:
                    self.screen.blit(self.dragged_object, tuple(self.dragged_object_pos))
                pygame.display.flip()

    def get_object_at_pos(self, pos) -> Optional[List[int]]:
        for row in range(8):
            for col in range(8):
                if self.board[row][col] is not None:  # If there's an image at this square
                    image_pos = [col * self.square_size, row * self.square_size]
                    # Check if the mouse is over the image
                    if pygame.Rect(*image_pos, self.square_size, self.square_size).collidepoint(pos):
                        print("Image selected for dragging")
                        return image_pos
        return None

    def right_button_clicked(self, square, pos):
        print(f"Square {square} clicked at position {pos}!")
        # Define the image path
        image_path = '../resources/images/pieces/pig.png'  # Replace with your actual image file path
        # Set the image at the clicked square
        self.set_image(square[1], square[0], image_path)


    def left_button_clicked(self, square, pos):
        print(f"Square {square} clicked at position {pos}!")
        clicked_color = (255, 0, 255) if ((square[1] + square[0]) % 2) == 0 else (0, 255, 255)

        # Check the current color of the square and change it to the other color
        if self.colors[square[1]][square[0]] == self.original_colors[(square[0] + square[1]) % 2]:
            self.change_square_color(square[1], square[0], clicked_color)
        else:
            self.change_square_color(square[1], square[0], self.original_colors[square[0]][square[1]])

    def change_square_color(self, row, col, new_color: Tuple[int, int, int]):
        print(f"Changing color of square ({row}, {col}) to {new_color}")
        self.colors[row][col] = new_color
        self.draw_board()
        pygame.display.flip()

    import time

    def make_move(self, start_square, end_square=(4, 4)):
        # Get the image at the start square
        dragged_object = self.board[start_square[1]][start_square[0]]
        if dragged_object is None:
            print(f"No image at square {start_square}")
            return

        distance = ((end_square[0] - start_square[0]) ** 2 + (end_square[1] - start_square[1]) ** 2) ** 0.5
        print(f"Moving image from {start_square} to {end_square} in {distance} steps")

        # Calculate the distance to move in each step
        dx = (end_square[0] - start_square[0]) * self.square_size / 50.0
        dy = (end_square[1] - start_square[1]) * self.square_size / 50.0


        # Remove the image from the start square
        self.board[start_square[1]][start_square[0]] = None

        # Move the image in small steps
        for i in range(50):
            # Update the position of the image
            self.dragged_object_pos = [start_square[0] * self.square_size + i * dx,
                                       start_square[1] * self.square_size + i * dy]
            # Redraw the board and the image
            self.screen.blit(dragged_object, tuple(map(int, self.dragged_object_pos)))
            self.draw_board()
            pygame.display.flip()
            # # Wait a short time
            time.sleep(0.0005)

            # Draw the board surface onto the screen
            self.screen.blit(self.board_surface, (0, 0))
            # If an image is being dragged, draw it at its current position
            # if self.dragging and self.dragged_object is not None:
            #     self.screen.blit(image, tuple(self.dragged_object_pos))
            # pygame.display.flip()



        # # Place the image on the end square
        self.board[end_square[1]][end_square[0]] = dragged_object
        #
        # self.draw_board()


if __name__ == "__main__":
    gui = ChessGUI()
    gui.draw_board()  # Draw the board once at the start
    gui.game_loop()  # Start the game loop
