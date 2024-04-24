

class ClickController:
    def __init__(self):
        self.board = [["[ ]" for _ in range(8)] for _ in range(8)]

    def click(self, x, y):
        print(f"Button clicked at ({x}, {y})")
        self.visualize_click_on_board(x,y)

    def visualize_click_on_board(self, x, y):
        # Set the clicked square
        self.board[x][y] = "[x]"

        # Print the chess board
        for row in self.board:
            print(" ".join(row))

        # Reset the clicked square
        self.board[x][y] = "[ ]"
