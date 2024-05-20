from abc import ABC, abstractmethod
import tkinter as tk


class ChessGuiAbs(tk.Tk, ABC):
    @abstractmethod
    def update_square_color(self, color, row, col):
        """Update the color of a specific square"""
        pass

    @abstractmethod
    def update_square_image(self, image_path, row, col):
        """Update the image of a piece at a specific square"""
        pass

    @abstractmethod
    def move_piece(self, name, row, col):
        """Move a piece to a specified location"""
        pass

    @abstractmethod
    def update_timer_label(self):
        """Update the timer label"""
        pass

    @abstractmethod
    def update_labels(self):
        """Update other labels"""
        pass