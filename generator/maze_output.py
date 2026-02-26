from typing import List, Tuple


class MazeOutput:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def write_maze(self, grid: List[List[int]],
                   entry: Tuple[int, int],
                   exit_pos: Tuple[int, int]) -> None:
        with open(self.filename, 'w') as f:
            for row in grid:
                hex_row = ''.join(f'{cell:X}' for cell in row)
                f.write(hex_row + '\n')
            f.write('\n')
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_pos[0]},{exit_pos[1]}\n")
            f.write("PLACEHOLDER_PATH\n")

        print(f"Maze written to: {self.filename}")
