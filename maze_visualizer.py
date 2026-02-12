#!/usr/bin/env python3

import subprocess
import sys
import tty
import termios


def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key


def read_output_file(filename: str):
    """
    Reads maze data from the output file

    Format:
    lines 1-n maze data (hexadecimal format)
    line  n+1 blank line
    line  n+2 start coordinates (row, col)
    line  n+3 end coordinates   (row, col)
    line  n+4 solution path (N/E/S/W)

    Returns:
    tuple: (maze_hex, start, end, path)
    """
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    maze_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line:
            break

        if ',' in line:
            parts = line.split(',')
            if len(parts) == 2:
                try:
                    int(parts[0].strip())
                    int(parts[1].strip())
                    break
                except ValueError:
                    pass
        maze_lines.append(line)
        i += 1

    # Parse maze - handle both space-separated and concatenated hex
    maze_hex = []
    for line_num, line in enumerate(maze_lines):
        if ' ' in line or '\t' in line:
            row = line.split()
        else:
            row = list(line)

        # Validate hex characters
        for col_num, char in enumerate(row):
            if char.upper() not in '0123456789ABCDEF':
                print(f"Warning: Invalid hex character '{char}' at row {line_num}, col {col_num}. Replacing with '0'.")
                row[col_num] = '0'

        maze_hex.append(row)

    # Check for consistent dimensions
    if maze_hex:
        row_lengths = [len(row) for row in maze_hex]
        min_len = min(row_lengths)
        max_len = max(row_lengths)

        if min_len != max_len:
            print(f"Warning: Inconsistent row lengths detected (min: {min_len}, max: {max_len})")
            print(f"Row lengths: {row_lengths}")
            print(f"Padding shorter rows to match the maximum length ({max_len})...")
            input("Press Enter to continue...")

            # Pad shorter rows with '0' (no walls)
            for row in maze_hex:
                while len(row) < max_len:
                    row.append('0')

    # Skip empty lines
    while i < len(lines) and not lines[i]:
        i += 1

    start = None
    if i < len(lines):
        parts = lines[i].split(',')
        start = (int(parts[0].strip()), int(parts[1].strip()))
        i += 1

    end = None
    if i < len(lines):
        parts = lines[i].split(',')
        end = (int(parts[0].strip()), int(parts[1].strip()))
        i += 1

    path = ""
    if i < len(lines):
        path = lines[i].strip()

    return maze_hex, start, end, path


def print_section(
    canvas,
    cam_y: int,
    cam_x: int,
    view_h: int,
    view_w: int,
    WALL_COLOR,
    FULL_CELL_COLOR,
    PATH_COLOR,
    START_COLOR,
    END_COLOR,
    RESET_COLOR,
    show_path: bool
) -> None:

    canvas_h = len(canvas)
    canvas_w = len(canvas[0])

    # Clamp camera so it never goes out of bounds
    cam_y = max(0, min(cam_y, canvas_h - view_h))
    cam_x = max(0, min(cam_x, canvas_w - view_w))

    for y in range(cam_y, cam_y + view_h):
        line = ""
        for x in range(cam_x, cam_x + view_w):
            ch = canvas[y][x]
            if ch == "L":
                line += FULL_CELL_COLOR + "  " + RESET_COLOR
            elif ch == "W":
                line += WALL_COLOR + "  " + RESET_COLOR
            elif ch == "S":
                line += START_COLOR + "  " + RESET_COLOR
            elif ch == "E":
                line += END_COLOR + "  " + RESET_COLOR
            elif ch == "P" and show_path:
                line += PATH_COLOR + "  " + RESET_COLOR
            else:
                line += "  "
        print(line)


def print_instructions() -> None:
    lines = [
        "c - switch color    x - change display size    p - show/hide path",
        "q - quit"
    ]

    width = max(len(line) for line in lines) + 2  # padding

    print("┌" + "─" * width + "┐")
    print("│ COMMANDS:" + " " * (width - len(" COMMANDS:")) + "│")
    print("├" + "─" * width + "┤")
    for line in lines:
        print(f"│ {line}" + " " * (width - len(line) - 1) + "│")
    print("└" + "─" * width + "┘")


def apply_path_to_canvas(canvas, start, path_str, H, W):
    """Mark the path on the canvas."""
    if not start or not path_str:
        return

    row, col = start

    # Mark start position
    y, x = 2*row + 1, 2*col + 1
    canvas[y][x] = "S"

    # Follow the path
    for direction in path_str:
        if direction == 'N':
            row -= 1
        elif direction == 'S':
            row += 1
        elif direction == 'E':
            col += 1
        elif direction == 'W':
            col -= 1

        # Mark the path on canvas
        if 0 <= row < H and 0 <= col < W:
            y, x = 2*row + 1, 2*col + 1
            if canvas[y][x] not in ["S", "E"]:
                canvas[y][x] = "P"

    # Mark end position
    y, x = 2*row + 1, 2*col + 1
    canvas[y][x] = "E"


def main() -> None:

    try:
        maze_hex, start, end, path = read_output_file("output.txt")
    except FileNotFoundError:
        print("Error: output file not found!")
        return
    except Exception as e:
        print(f"Error reading output file: {e}")
        return

    view_height = 40
    view_width = 40
    H = len(maze_hex)
    W = len(maze_hex[0])
    canvas_height = 2 * H + 1
    canvas_width = 2 * W + 1
    cam_y = 0
    cam_x = 0
    show_path = False

    canvas = [[" " for _ in range(canvas_width)] for _ in range(canvas_height)]

    # Fill walls and cells
    for r in range(H):
        for c in range(W):
            cell = int(maze_hex[r][c], 16)
            y, x = 2*r + 1, 2*c + 1

            if cell == 0xF:
                canvas[y][x] = "L"  # FILLED CELL
            else:
                canvas[y][x] = " "  # CENTER

            # Wall bits
            north = bool(cell & 1)
            east = bool(cell & 2)
            south = bool(cell & 4)
            west = bool(cell & 8)

            # Fill direct walls
            if north:
                canvas[y-1][x] = "W"
            if south:
                canvas[y+1][x] = "W"
            if east:
                canvas[y][x+1] = "W"
            if west:
                canvas[y][x-1] = "W"

            # Junctions if any wall touches corner
            if north or west:   canvas[y-1][x-1] = "W"
            if north or east:   canvas[y-1][x+1] = "W"
            if south or west:   canvas[y+1][x-1] = "W"
            if south or east:   canvas[y+1][x+1] = "W"

    # Outer walls
    for i in range(canvas_height):
        canvas[i][0] = "W"
        canvas[i][-1] = "W"
    for j in range(canvas_width):
        canvas[0][j] = "W"
        canvas[-1][j] = "W"

    # Apply path to canvas
    apply_path_to_canvas(canvas, start, path, H, W)

    # Color definitions
    COLORS = {
        "RED": "\033[41m",
        "BLUE": "\033[44m",
        "GREEN": "\033[42m",
        "YELLOW": "\033[43m",
        "MAGENTA": "\033[45m",
        "CYAN": "\033[46m",
        "RESET": "\033[0m",
    }

    colors = {
        "WALL": "\033[41m",
        "FILL": "\033[0m",
        "LOGO": "\033[44m",
        "PATH": "\033[43m",
        "START": "\033[42m",
        "END": "\033[45m",
    }

    while True:
        print_section(
            canvas,
            cam_y,
            cam_x,
            view_height,
            view_width,
            colors["WALL"],
            colors["LOGO"],
            colors["PATH"],
            colors["START"],
            colors["END"],
            COLORS["RESET"],
            show_path
        )
        print_instructions()

        key = get_key()

        subprocess.run(["clear"])

        match key:
            case "q":
                break
            case "p":
                show_path = not show_path
            case "c":
                target = input("Change which color? (WALL / FILL / LOGO / PATH / START / END): ").upper()
                if target not in colors:
                    print("Invalid target")
                    continue
                color = input(f"Select color ({', '.join(COLORS)}): ").upper()
                if color not in COLORS:
                    print("Invalid color")
                    continue
                colors[target] = COLORS[color]
            case "x":
                try:
                    target_size = int(input("ENTER DISPLAY SIZE (HEIGHT): "))
                    if target_size > 10:
                        print(f"Height set to {target}")
                        view_height = target_size
                except Exception:
                    print("Invalid input!")
                    continue
                try:
                    target_size = int(input("ENTER DISPLAY SIZE (WIDTH): "))
                    if target_size > 10:
                        print(f"Width set to {target}")
                        view_width = target_size
                except Exception:
                    print("Invalid input!")
                    continue
                if view_height > canvas_height:
                    view_height = canvas_height
                if view_width > canvas_width:
                    view_width = canvas_width

            case "w":
                cam_y -= 1
            case "s":
                cam_y += 1
            case "a":
                cam_x -= 1
            case "d":
                cam_x += 1
        cam_y = max(0, min(cam_y, canvas_height - view_height))
        cam_x = max(0, min(cam_x, canvas_width - view_width))


if __name__ == "__main__":
    main()
