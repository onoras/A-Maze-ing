import random
from typing import Tuple, Set
from ..maze_gen import MazeGenerator


class DFSAlgorithm(MazeGenerator):
    def __init__(self, width: int, height: int, seed: int) -> None:
        super().__init__(width, height, seed)
        if seed is not None:
            random.seed(seed)
        self.visited: Set[Tuple[int, int]] = set()

    def _generate_paths(self):
        return super()._generate_paths()
