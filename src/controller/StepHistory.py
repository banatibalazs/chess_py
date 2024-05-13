from typing import List, Dict

from src.model.Color import Color
from src.model.PieceType import PieceType


class StepHistory:
    def __init__(self) -> None:
        self.steps: List[str] = []
        self._column_map: Dict[int, str] = {
            0: 'a',
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h'
        }
        self._reverse_column_map = {v: k for k, v in self._column_map.items()}

    def add_step(self, piece_type: PieceType, piece_color: Color,
                 from_row: int, from_col: int, to_row: int, to_col: int) -> None:

        self.steps.append(f"{piece_color} {piece_type} {self._column_map[from_col]}{8 - from_row} -> "
                          f"{self._column_map[to_col]}{8 - to_row}")

    def get_steps(self) -> List[str]:
        return self.steps

    def clear(self) -> None:
        self.steps = []

    def __str__(self) -> str:
        return str(self.steps)
