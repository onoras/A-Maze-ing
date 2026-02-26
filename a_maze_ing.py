import sys
from generator import ConfigParser, MazeGenerator, MazeOutput


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        print("Parsing configuration...")
        parser = ConfigParser(config_file)
        parser.parse()

        width, height = parser.get_dimensions()
        entry = parser.get_entry()
        exit_pos = parser.get_exit()
        output_file = parser.get_output_file()
        algo = parser.get_algo()

        print("Configuration loaded:")
        print(f"  Dimensions: {width}x{height}")
        print(f"  Entry: {entry}")
        print(f"  Exit: {exit_pos}")
        print(f"  Output: {output_file}")
        print(f"  Algorithm: {algo}")
        generator = MazeGenerator(width, height, algo)
        generator.set_entry_exit(entry, exit_pos)
        grid = generator.generate()
        output = MazeOutput(output_file)
        output.write_maze(grid, entry, exit_pos)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
