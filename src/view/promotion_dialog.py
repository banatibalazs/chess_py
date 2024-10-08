from src.model.enums.piece_type import PieceType
import tkinter as tk

from src.view.square import Square


class PromotionDialog(tk.Toplevel):
    def __init__(self, queen_image_path, rook_image_path, bishop_image_path, knight_image_path) -> None:
        super().__init__()
        self.title("Promotion")
        self.geometry("360x175")
        self.resizable(False, False)

        self._queen_image_path: str = queen_image_path
        self._rook_image_path: str = rook_image_path
        self._bishop_image_path: str = bishop_image_path
        self._knight_image_path: str = knight_image_path

        self._piece_type: PieceType = PieceType.QUEEN

        self._label: tk.Label = tk.Label(self, text="Choose a piece:")
        self._label.pack()

        self._frame: tk.Frame = tk.Frame(self)
        self._frame.pack()

        self._rook_button: Square = Square(self, width=8, height=4, onclick=self._on_rook, col=0, row=0)
        self._rook_button.pack(side=tk.LEFT)
        self._rook_button.set_image(self._rook_image_path)

        self._bishop_button: Square = Square(self, width=8, height=4, onclick=self._on_bishop, col=1, row=0)
        self._bishop_button.pack(side=tk.LEFT)
        self._bishop_button.set_image(self._bishop_image_path)

        self._knight_button: Square = Square(self, width=8, height=4, onclick=self._on_knight, col=2, row=0)
        self._knight_button.pack(side=tk.LEFT)
        self._knight_button.set_image(self._knight_image_path)

        self._queen_button: Square = Square(self, width=8, height=4, onclick=self._on_queen, col=3, row=0)
        self._queen_button.pack(side=tk.LEFT)
        self._queen_button.set_image(self._queen_image_path)

    def _on_rook(self, *args) -> None:
        self._piece_type = PieceType.ROOK
        self.destroy()

    def _on_bishop(self, *args) -> None:
        self._piece_type = PieceType.BISHOP
        self.destroy()

    def _on_knight(self, *args) -> None:
        self._piece_type = PieceType.KNIGHT
        self.destroy()

    def _on_queen(self, *args) -> None:
        self._piece_type = PieceType.QUEEN
        self.destroy()

    def get_type(self, *args) -> PieceType:
        return self._piece_type