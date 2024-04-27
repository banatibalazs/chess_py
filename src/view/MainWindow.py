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
        self.white_player_name = None
        self.black_player_name = None
        self.start_button = None
        self.exit_button = None
        self.result_label = None
        self.setup_ui()

    def setup_ui(self) -> None:
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

        white_player_name_label = tk.Label(frame, text="WhitePlayer:",
                                        background="#FFFFFF",
                                        font=('Helvetica', MainWindow.TEXT_SIZE, 'bold'))
        white_player_name_label.grid(row=1, column=0, sticky="e", pady=MainWindow.LABEL_PADDING)

        self.white_player_name = tk.Entry(frame)
        self.white_player_name.insert(0, "Player1")
        self.white_player_name.grid(row=1, column=1, sticky="w", padx=5)

        black_player_name_label = tk.Label(frame, text="BlackPlayer:",
                                        background="#FFFFFF",
                                        font=('Helvetica', MainWindow.TEXT_SIZE, 'bold'))
        black_player_name_label.grid(row=2, column=0, sticky="e")

        self.black_player_name = tk.Entry(frame)
        self.black_player_name.insert(0, "Player2")
        self.black_player_name.grid(row=2, column=1, sticky="w", padx=5)

        start_button = tk.Button(frame, text="Start Game",
                                command=self.open_new_window,
                                background= "#CCFFCC",
                                image=start_button_image_tk,
                                foreground='white',
                                font=('Helvetica', 16),
                                borderwidth=2,
                                relief="groove",
                                width=250,
                                height=75)
        start_button.image = start_button_image_tk
        start_button.grid(row=3, column=0, columnspan=2, pady=(40, 10))

        # Bind the <Enter> and <Leave> events to the button
        start_button.bind("<Enter>", self.on_enter_startButton)
        start_button.bind("<Leave>", self.on_leave_startButton)

        exit_button = tk.Button(frame, text="Exit",
                                command=self.exit_button_click,
                                background= "#FFFFFF",
                                foreground='black',
                                font=('Helvetica', 16),
                                borderwidth=2,
                                relief="groove",
                                width=20,
                                height=1
                               )
        exit_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Bind the <Enter> and <Leave> events to the button
        exit_button.bind("<Enter>", self.on_enter_exitButton)
        exit_button.bind("<Leave>", self.on_leave_exitButton)

        self.result_label = tk.Label(frame, text="Welcome to this game!")
        self.result_label.grid(row=5, column=0, columnspan=2)

    def open_new_window(self):
        chess_window = ChessWindow("Chess Game",
                                  self.white_player_name.get(),
                                  self.black_player_name.get())
        chess_window.run()

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



