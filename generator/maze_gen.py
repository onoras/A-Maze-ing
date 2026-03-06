from typing import List, Tuple
from abc import ABC, abstractmethod


class MazeGenerator(ABC):
    """
    Abstract base Class for maze Generators
    """
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(self, width: int, height: int, seed: int,
                 perfect: bool) -> None:
        """
        Initialize maze generator.
        Args:
            width: Maze width in cells
            height: Maze height in cells
            seed: Random seed for reproducibility
        """
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive")
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.grid: List[List[int]] = []
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (width - 1, height - 1)

    def set_entry_exit(self, entry_pos: Tuple[int, int],
                       exit_pos: Tuple[int, int]) -> None:
        """
        Checks and sets entry and exit points

        entry_pos: Entry coordinates (col, row)
        exit_pos: Exit coordinates (col, row)
        """
        if entry_pos == exit_pos:
            raise ValueError("Entry and exit must be different")
        entry_col, entry_row = entry_pos
        exit_col, exit_row = exit_pos
        if not (0 <= entry_col < self.width and 0 <= entry_row < self.height):
            raise ValueError(f"Entry {entry_pos} out of bounds")
        if not (0 <= exit_col < self.width and 0 <= exit_row < self.height):
            raise ValueError(f"Exit {exit_pos} out of bounds")
        self.entry = entry_pos
        self.exit = exit_pos

    @abstractmethod
    def _generate_paths(self, obstacle_cells: List[Tuple[int, int]] = None):
        """
        Generate maze paths using specific algorithms in the subclasses
        """
        pass

    def generate(self) -> List[List[int]]:
        self.grid = [[15 for _ in range(self.width)] for _ in
                     range(self.height)]
        pattern_cells = []
        if self.width >= 7 and self.height >= 5:
            pattern_cells = self._create_42_pattern()
        self._generate_paths(pattern_cells)
        self._create_outer_walls()
        return self.grid

    def _create_outer_walls(self) -> None:
        """
        Ensure external borders have walls (except at entry/exit).
        """
        entry_col, entry_row = self.entry
        exit_col, exit_row = self.exit

        for col in range(self.width):
            if not (entry_row == 0 and entry_col == col) and \
               not (exit_row == 0 and exit_col == col):
                self.grid[0][col] |= self.NORTH

        for col in range(self.width):
            if not (entry_row == self.height - 1 and entry_col == col) and \
               not (exit_row == self.height - 1 and exit_col == col):
                self.grid[self.height - 1][col] |= self.SOUTH

        for row in range(self.height):
            if not (entry_col == 0 and entry_row == row) and \
               not (exit_col == 0 and exit_row == row):
                self.grid[row][0] |= self.WEST

        for row in range(self.height):
            if not (entry_col == self.width - 1 and entry_row == row) and \
               not (exit_col == self.width - 1 and exit_row == row):
                self.grid[row][self.width - 1] |= self.EAST

    def _create_42_pattern(self) -> List[Tuple[int, int]]:
        """
        Add 42 pattern made of fully closed cells in the center.
        """
        center_col = (self.width - 7) // 2
        center_row = (self.height - 5) // 2

        four_pattern = [
            [1, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
            [0, 0, 1],
            [0, 0, 1],
        ]

        two_pattern = [
            [1, 1, 1],
            [0, 0, 1],
            [1, 1, 1],
            [1, 0, 0],
            [1, 1, 1],
        ]
        pattern_cells = []
        for row_offset in range(5):
            for col_offset in range(3):
                if four_pattern[row_offset][col_offset] == 1:
                    row = center_row + row_offset
                    col = center_col + col_offset - 1
                    if 0 <= row < self.height and 0 <= col < self.width:
                        self.grid[row][col] = 15
                        pattern_cells.append((row, col))
        for row_offset in range(5):
            for col_offset in range(3):
                if two_pattern[row_offset][col_offset] == 1:
                    row = center_row + row_offset
                    col = center_col + col_offset + 4
                    if 0 <= row < self.height and 0 <= col < self.width:
                        self.grid[row][col] = 15
                        pattern_cells.append((row, col))
        return pattern_cells

    def get_grid(self) -> List[List[int]]:
        return self.grid

    def _remove_wall(self, row: int, col: int, direction: int) -> None:
        """
        Removes Wall from a cell by flipping ~ the bits of the cell
        """
        self.grid[row][col] &= ~direction

    def _get_opposite(self, direction: int) -> int:
        """
        Get opposite Direction
        """
        opposites = {
            self.NORTH: self.SOUTH,
            self.SOUTH: self.NORTH,
            self.WEST: self.EAST,
            self.EAST: self.WEST
        }
        return opposites[direction]
