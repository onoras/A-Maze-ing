import random
from typing import Tuple, Set, List
from ..maze_gen import MazeGenerator


class DFSAlgorithm(MazeGenerator):
    def __init__(self, width: int, height: int, seed: int,
                 perfect: bool) -> None:
        super().__init__(width, height, seed, perfect)
        self.random = random.Random(seed)
        self.visited: Set[Tuple[int, int]] = set()

    def _generate_paths(self,  obstacle_cells: List[Tuple[int, int]] = None):
        """Generate maze using recursive backtracker (DFS)"""
        self.visited.clear()
        if obstacle_cells:
            self.visited.update(obstacle_cells)
        start_col, start_row = self.entry
        start_pos = (start_row, start_col)
        if start_pos in self.visited:
            raise ValueError("Entry cannot be inside obstacle pattern")
        stack = [start_pos]
        self.visited.add(start_pos)
        while stack:
            row, col = stack[-1]
            neighbors = self._get_unvisited_neighbors(row, col)
            self.random.shuffle(neighbors)
            if neighbors:
                next_row, next_col, direction = neighbors[0]
                self._remove_wall_between(row, col, next_row, next_col,
                                          direction)
                self.visited.add((next_row, next_col))
                stack.append((next_row, next_col))
            else:
                stack.pop()

    def _get_unvisited_neighbors(self, row: int,
                                 col: int) -> List[Tuple[int, int, int]]:
        neighbors: List[Tuple[int, int, int]] = []
        if row > 0 and (row - 1, col) not in self.visited:
            neighbors.append((row - 1, col, self.NORTH))
        if col < self.width - 1 and (row, col + 1) not in self.visited:
            neighbors.append((row, col + 1, self.EAST))
        if row < self.height - 1 and (row + 1, col) not in self.visited:
            neighbors.append((row + 1, col, self.SOUTH))
        if col > 0 and (row, col - 1) not in self.visited:
            neighbors.append((row, col - 1, self.WEST))
        return neighbors

    def _remove_wall_between(self, row1: int, col1: int,
                             row2: int, col2: int, direction: int) -> None:
        self.grid[row1][col1] &= ~direction
        opposite = self._get_opposite(direction)
        self.grid[row2][col2] &= ~opposite
