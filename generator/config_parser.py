from typing import Dict, Tuple
import random


class ConfigParser:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.config: Dict[str, str] = {}

    def validate_config(self) -> None:
        required_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
                         'OUTPUT_FILE', 'PERFECT', 'ALGORITHM']
        missing = [key for key in required_keys if key not in self.config]
        if missing:
            raise ValueError

    def parse(self) -> Dict[str, str]:
        try:
            with open(self.filepath, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' not in line:
                        raise ValueError(
                            f"Line {line_num}: Invalid Format. "
                            f"Expected Key=Value, got {line}"
                        )
                    key, value = line.split('=', 1)
                    self.config[key.strip()] = value.strip()
            self.validate_config()
            return self.config
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {self.filepath}")

    def get_dimensions(self) -> Tuple[int, int]:
        width = int(self.config['WIDTH'])
        height = int(self.config['HEIGHT'])

        entry = self.get_entry()
        exit = self.get_exit()
        entry_x, entry_y = entry
        exit_x, exit_y = exit

        if entry == exit:
            raise ValueError("Entry and Exit can't have the same Coordinates")

        if not (0 <= entry_x < width and 0 <= entry_y < height):
            raise ValueError("Entry point out of bounds")

        if not (0 <= exit_x < width and 0 <= exit_y < height):
            raise ValueError("Exit point out of bounds")

        if width <= 0 or height <= 0:
            raise ValueError("Width and Height must be positive integers")

        return width, height

    def get_entry(self) -> Tuple[int, int]:
        x, y = self.config['ENTRY'].split(',')
        return int(x.strip()), int(y.strip())

    def get_exit(self) -> Tuple[int, int]:
        x, y = self.config['EXIT'].split(',')
        return int(x.strip()), int(y.strip())

    def get_output_file(self) -> str:
        return self.config['OUTPUT_FILE']

    def is_perfect(self) -> bool:
        return self.config['PERFECT'].lower() == 'true'

    def get_algo(self) -> str:
        if self.config['ALGORITHM'] == 'DFS':
            return "DFS"
        elif self.config['ALGORITHM'] == 'PRIM':
            return "PRIM"
        else:
            raise ValueError("No correct Algorithm")

    def get_seed(self) -> int:
        if 'SEED' in self.config and self.config['SEED']:
            return int(self.config['SEED'])
        else:
            return random.randint(1, 100000)
