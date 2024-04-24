import tkinter as tk
from PIL import Image, ImageTk


from src.view.ChessWindow import ChessWindow


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Welcome to Chess Game!")
        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()

        img = Image.open("chess.png")
        imgtk = ImageTk.PhotoImage(img)
        # Create a label and add the image to it
        image_label = tk.Label(frame, image=imgtk)
        image_label.image = imgtk  # keep a reference to the image
        image_label.grid(row=0, column=0, columnspan=2)

        whitePlayerNameLabel = tk.Label(frame, text="WhitePlayer:")
        whitePlayerNameLabel.grid(row=1, column=0, sticky="w")

        self.whitePlayerName = tk.Entry(frame)
        self.whitePlayerName.grid(row=1, column=1, sticky="w", padx=5)

        blackPlayerNameLabel = tk.Label(frame, text="BlackPlayer:")
        blackPlayerNameLabel.grid(row=2, column=0, sticky="w")


        self.blackPlayerName = tk.Entry(frame)
        self.blackPlayerName.grid(row=2, column=1, sticky="w", padx=5)

        startButton = tk.Button(frame, text="Start Game",
                                command=self.open_new_window,
                                background= "#445566",
                                foreground='white',
                                font=('Helvetica', 16),
                                borderwidth=2,
                                relief="groove")
        startButton.grid(row=3, column=0, columnspan=2, pady=(40, 10))

        exitButton = tk.Button(frame, text="Exit",
                                command=self.exit_button_click,
                                background= "#f122f1",
                                foreground='white',
                                font=('Helvetica', 16),
                                borderwidth=2,
                                relief="groove")
        exitButton.grid(row=4, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(frame, text="Welcome to this game!")
        self.result_label.grid(row=5, column=0, columnspan=2)

    def open_new_window(self):
        chessWindow = ChessWindow("Chess Game")
        chessWindow.run()

    def run(self):
        self.root.mainloop()

    def exit_button_click(self):
        self.root.destroy()



