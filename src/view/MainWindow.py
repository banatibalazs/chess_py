import tkinter as tk
from PIL import Image, ImageTk


from src.view.ChessWindow import ChessWindow


class MainWindow:

    CHESS_GAME_IMAGE_PATH = "../resources/images/welcome_page/chess-draw.png"
    START_BUTTON_IMAGE_PATH = "../resources/images/welcome_page/start.png"
    TEXT_SIZE = 14
    LABEL_PADDING = (10, 10)

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Welcome to Chess Game!")
        self.root.configure(background="#FFFFFF")
        self.setup_ui()


    def setup_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.configure(background="#FFFFFF")
        frame.pack()

        chess_image = Image.open(MainWindow.CHESS_GAME_IMAGE_PATH)
        start_button_image = Image.open(MainWindow.START_BUTTON_IMAGE_PATH)

        # Resize the images
        chess_image = chess_image.resize((400, 200))
        start_button_image = start_button_image.resize((75, 75))

        chess_image_tk = ImageTk.PhotoImage(chess_image)
        start_button_image_tk = ImageTk.PhotoImage(start_button_image)

        # Create a label and add the image to it
        image_label = tk.Label(frame, image=chess_image_tk)
        image_label.image = chess_image_tk  # keep a reference to the image
        image_label.grid(row=0, column=0, columnspan=2)

        whitePlayerNameLabel = tk.Label(frame, text="WhitePlayer:",
                                        background="#FFFFFF",
                                        font=('Helvetica', MainWindow.TEXT_SIZE, 'bold'))
        whitePlayerNameLabel.grid(row=1, column=0, sticky="e", pady=MainWindow.LABEL_PADDING)

        self.whitePlayerName = tk.Entry(frame)
        self.whitePlayerName.insert(0, "Player1")
        self.whitePlayerName.grid(row=1, column=1, sticky="w", padx=5)

        blackPlayerNameLabel = tk.Label(frame, text="BlackPlayer:",
                                        background="#FFFFFF",
                                        font=('Helvetica', MainWindow.TEXT_SIZE, 'bold'))
        blackPlayerNameLabel.grid(row=2, column=0, sticky="e")


        self.blackPlayerName = tk.Entry(frame)
        self.blackPlayerName.insert(0, "Player2")
        self.blackPlayerName.grid(row=2, column=1, sticky="w", padx=5)

        startButton = tk.Button(frame, text="Start Game",
                                command=self.open_new_window,
                                background= "#CCFFCC",
                                image=start_button_image_tk,
                                foreground='white',
                                font=('Helvetica', 16),
                                borderwidth=2,
                                relief="groove",
                                width=250,
                                height=75)
        startButton.image = start_button_image_tk
        startButton.grid(row=3, column=0, columnspan=2, pady=(40, 10))

        # Bind the <Enter> and <Leave> events to the button
        startButton.bind("<Enter>", self.on_enter_startButton)
        startButton.bind("<Leave>", self.on_leave_startButton)

        exitButton = tk.Button(frame, text="Exit",
                                command=self.exit_button_click,
                                background= "#FFFFFF",
                                foreground='black',
                                font=('Helvetica', 16),
                                borderwidth=2,
                                relief="groove",
                                width=20,
                                height=1
                               )
        exitButton.grid(row=4, column=0, columnspan=2, pady=10)

        # Bind the <Enter> and <Leave> events to the button
        exitButton.bind("<Enter>", self.on_enter_exitButton)
        exitButton.bind("<Leave>", self.on_leave_exitButton)

        self.result_label = tk.Label(frame, text="Welcome to this game!")
        self.result_label.grid(row=5, column=0, columnspan=2)

    def open_new_window(self):
        chessWindow = ChessWindow("Chess Game", self.whitePlayerName.get(), self.blackPlayerName.get())
        chessWindow.run()

    def run(self):
        self.root.mainloop()

    def exit_button_click(self):
        self.root.destroy()

    def on_enter_startButton(self, event):
        # Change the style of the button when the mouse pointer enters it
        event.widget.config(background="#88FF88")

    def on_leave_startButton(self, event):
        # Change the style of the button back to the original when the mouse pointer leaves it
        event.widget.config(background="#CCFFCC")

    def on_enter_exitButton(self, event):
        # Change the style of the button when the mouse pointer enters it
        event.widget.config(background="#CCCCCC")

    def on_leave_exitButton(self, event):
        # Change the style of the button back to the original when the mouse pointer leaves it
        event.widget.config(background="#FFFFFF")



