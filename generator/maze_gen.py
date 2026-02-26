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

    def __init__(self, width: int, height: int, seed: int) -> None:
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
        self.grid: List[List[int]] = []
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (width - 1, height - 1)

    def set_entry_exit(self, entry_pos: Tuple[int, int],
                       exit_pos: Tuple[int, int]) -> None:
        """
        Checks and sets entry and exit points

        entry_pos: Entry coordinates (x, y)
        exit_pos: Exit coordinates (x, y)
        """
        if entry_pos == exit_pos:
            raise ValueError("Entry and exit must be different")
        ex, ey = entry_pos
        xx, xy = exit_pos
        if not (0 <= ex < self.width and 0 <= ey < self.height):
            raise ValueError(f"Entry {entry_pos} out of bounds")
        if not (0 <= xx < self.width and 0 <= xy < self.height):
            raise ValueError(f"Exit {exit_pos} out of bounds")
        self.entry = entry_pos
        self.exit = exit_pos

    @abstractmethod
    def _generate_paths(self) -> None:
        """
        Generate maze paths using specific algorithms in the subclasses
        """
        pass

    def generate(self) -> List[List[int]]:
        self._generate_paths()
        self._create_outer_walls()
        if self.width >= 7 and self.height >= 5:
            self._create_42_pattern()

        return self.grid

    def _create_outer_walls(self) -> None:
        for x in range(self.width):
            if (x, 0) != self.entry:
                self.grid[0][x] |= self.NORTH

        for x in range(self.width):
            if (x, self.height - 1) != self.exit:
                self.grid[self.height - 1][x] |= self.SOUTH

        for y in range(self.height):
            if (0, y) != self.entry:
                self.grid[y][0] |= self.WEST

        for y in range(self.height):
            if (self.width - 1, y) != self.exit:
                self.grid[y][self.width - 1] |= self.EAST

    def _create_42_pattern(self) -> None:
        center_x = (self.width - 7) // 2
        center_y = (self.height - 5) // 2

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
        for dy in range(5):
            for dx in range(3):
                if four_pattern[dy][dx] == 1:
                    y = center_y + dy
                    x = center_x + dx - 1
                    if 0 <= y < self.height and 0 <= x < self.width:
                        self.grid[y][x] = 15
        for dy in range(5):
            for dx in range(3):
                if two_pattern[dy][dx] == 1:
                    y = center_y + dy
                    x = center_x + dx + 4
                    if 0 <= y < self.height and 0 <= x < self.width:
                        self.grid[y][x] = 15

    def get_grid(self) -> List[List[int]]:
        return self.grid

    def _remove_wall(self, x: int, y: int, direction: int) -> None:
        """
        Removes Wall from a cell by flipping ~ the bits of the cell
        """
        self.grid[x][y] &= ~direction

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
