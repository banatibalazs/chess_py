import tkinter as tk
from PIL import Image, ImageTk

from src.model.GameResult import GameResult


class EndGameDialog(tk.Toplevel):
    CHESS_TIME_IMAGE_PATH = "../resources/images/welcome_page/chess-clock.png"
    def __init__(self, gameResult: GameResult):
        tk.Toplevel.__init__(self)
        self.title("Game Over")
        self.geometry("300x200")
        self.resizable(False, False)
        self._label: tk.Label = tk.Label(self, text=f"{gameResult.name}", font=('Helvetica', 12, 'bold'))
        self._label.pack()

        if gameResult == GameResult.WHITE_WON_BY_TIMEOUT or gameResult == GameResult.BLACK_WON_BY_TIMEOUT:
            image = Image.open(EndGameDialog.CHESS_TIME_IMAGE_PATH)
            image = image.resize((100, 100))
            photo = ImageTk.PhotoImage(image)
            self._img_label: tk.Label = tk.Label(self, image=photo)
            self._img_label.image = photo
            self._img_label.pack()

        self._button: tk.Button = tk.Button(self, text="OK", command=self.destroy, font=('Helvetica', 10, 'bold'), width=10, height=2)
        self._button.pack()