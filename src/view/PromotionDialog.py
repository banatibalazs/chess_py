from src.model.PieceType import PieceType
import tkinter as tk

class PromotionDialog:
    def __init__(self, root) -> None:
        self._root: tk.Toplevel = root
        self._root.title("Promotion")
        self._root.geometry("200x200")
        self._root.resizable(False, False)

        self._piece_type: PieceType = PieceType.QUEEN

        self._label: tk.Label = tk.Label(self._root, text="Choose a piece:")
        self._label.pack()

        self._frame: tk.Frame = tk.Frame(self._root)
        self._frame.pack()

        self._rook_button: tk.Button = tk.Button(self._frame, text="Rook", command=self._on_rook)
        self._rook_button.pack(side=tk.LEFT)

        self._bishop_button: tk.Button = tk.Button(self._frame, text="Bishop", command=self._on_bishop)
        self._bishop_button.pack(side=tk.LEFT)

        self._knight_button: tk.Button = tk.Button(self._frame, text="Knight", command=self._on_knight)
        self._knight_button.pack(side=tk.LEFT)

        self._queen_button: tk.Button = tk.Button(self._frame, text="Queen", command=self._on_queen)
        self._queen_button.pack(side=tk.LEFT)

    def _on_rook(self) -> None:
        self._piece_type = PieceType.ROOK
        self._root.destroy()

    def _on_bishop(self) -> None:
        self._piece_type = PieceType.BISHOP
        self._root.destroy()

    def _on_knight(self) -> None:
        self._piece_type = PieceType.KNIGHT
        self._root.destroy()

    def _on_queen(self) -> None:
        self._piece_type = PieceType.QUEEN
        self._root.destroy()

    def get_type(self) -> PieceType:
        return self._piece_type