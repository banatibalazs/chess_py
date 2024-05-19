import pygame


class ChessGUI:
    def __init__(self, screen_width=800, screen_height=800):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Chess Game")
        self.square_size = screen_width // 8  # Assuming board is 8x8
        self.running = True
        self.rects = [
            [pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size) for col in
             range(8)] for row in range(8)]
        self.board_surface = pygame.Surface((screen_width, screen_height))
        self.colors = [[(233, 236, 239) if (row + col) % 2 == 0 else (125, 135, 150) for col in range(8)] for row in range(8)]  # Light and dark square colors
        self.original_colors = [[(233, 236, 239) if (row + col) % 2 == 0 else (125, 135, 150) for col in range(8)] for
                                row in range(8)]  # Store the original colors
        self.dragging = False  # Indicates whether we're currently dragging an object
        self.dragged_object = None  # The object that is being dragged
        # ... existing code ...
        self.images = [pygame.image.load('../resources/images/welcome_page/chess-clock.png') for _ in
                       range(8)]  # Load the images
        self.images = [pygame.transform.scale(image, (self.square_size, self.square_size)) for image in
                       self.images]  # Scale the images to fit the square
        self.images_pos = [[col * self.square_size, 0] for col in range(8)]  # The positions of the images

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(self.board_surface, self.colors[row][col],
                                 pygame.Rect(col * self.square_size, row * self.square_size, self.square_size,
                                             self.square_size))
        for i, image_pos in enumerate(self.images_pos):
            self.board_surface.blit(self.images[i], tuple(image_pos))

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Start dragging
                    self.dragging = True
                    self.dragged_object = self.get_object_at_pos(event.pos)
                    self.original_pos = self.dragged_object.copy()  # Store the original position
                    # Store the original square coordinates
                    self.original_square = (
                    self.dragged_object[0] // self.square_size, self.dragged_object[1] // self.square_size)
                    # Change the color of the square that the image was on
                    self.change_square_color(self.original_square[1], self.original_square[0],
                                             (255, 0, 0))  # Change to red color
                elif event.type == pygame.MOUSEMOTION:
                    # If we're dragging an object, update its position to follow the mouse
                    if self.dragging and self.dragged_object is not None:
                        new_x = event.pos[0] - self.square_size // 2
                        new_y = event.pos[1] - self.square_size // 2
                        # Check if the new position is within the board
                        if 0 <= new_x + self.square_size // 2 < 8 * self.square_size and 0 <= new_y + self.square_size // 2 < 8 * self.square_size:
                            self.dragged_object[0] = new_x
                            self.dragged_object[1] = new_y
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Stop dragging
                    self.dragging = False
                    # Snap the image to the center of the square it is above
                    square_x = (self.dragged_object[0] + self.images[0].get_width() // 2) // self.square_size
                    square_y = (self.dragged_object[1] + self.images[0].get_height() // 2) // self.square_size
                    # Check if the new position is within the board
                    if 0 <= square_x < 8 and 0 <= square_y < 8:
                        self.dragged_object[0] = square_x * self.square_size + self.square_size // 2 - self.images[
                            0].get_width() // 2
                        self.dragged_object[1] = square_y * self.square_size + self.square_size // 2 - self.images[
                            0].get_height() // 2
                    else:
                        # If the new position is not within the board, reset the position of the image to its original position
                        self.dragged_object = self.original_pos
                    # Change the color of the original square back to its original color
                    self.change_square_color(self.original_square[1], self.original_square[0],
                                             self.original_colors[self.original_square[1]][self.original_square[0]])
                    self.dragged_object = None

            self.draw_board()
            self.screen.blit(self.board_surface, (0, 0))
            pygame.display.flip()

    def get_object_at_pos(self, pos):
        for image_pos in self.images_pos:
            if pygame.Rect(*image_pos, self.square_size, self.square_size).collidepoint(pos):
                print("Image selected for dragging")
                return image_pos
        return None

    def right_button_clicked(self, square, pos):
        print(f"Square {square} clicked at position {pos}!")
        # Define the color you want to change to when clicked
        clicked_color = (255, 0, 0)  # Red color

        # Check the current color of the square and change it to the other color
        if self.colors[square[0]][square[1]] == self.original_colors[square[0]][square[1]]:
            self.change_square_color(square[0], square[1], clicked_color)
        else:
            self.change_square_color(square[0], square[1], self.original_colors[square[0]][square[1]])

    def left_button_clicked(self, square, pos):
        print(f"Square {square} clicked at position {pos}!")
        clicked_color = (255, 0, 255)  # Red color

        # Check the current color of the square and change it to the other color
        if self.colors[square[0]][square[1]] == self.original_colors[square[0]][square[1]]:
            self.change_square_color(square[0], square[1], clicked_color)
        else:
            self.change_square_color(square[0], square[1], self.original_colors[square[0]][square[1]])


    # ... existing methods ...

    def change_square_color(self, row, col, new_color):
        self.colors[row][col] = new_color
        self.draw_board()
        pygame.display.flip()

if __name__ == "__main__":
    gui = ChessGUI()
    gui.draw_board()  # Draw the board once at the start
    gui.game_loop()
    # gui.change_square_color(0, 0, (255, 255, 0))