

def print_section(
    canvas,
    cam_y,
    cam_x,
    view_h,
    view_w,
    WALL_COLOR,
    FULL_CELL_COLOR,
    RESET_COLOR
):
    canvas_h = len(canvas)
    canvas_w = len(canvas[0])

    # Clamp camera so it never goes out of bounds
    cam_y = max(0, min(cam_y, canvas_h - view_h))
    cam_x = max(0, min(cam_x, canvas_w - view_w))

    for y in range(cam_y, cam_y + view_h):
        line = ""
        for x in range(cam_x, cam_x + view_w):
            ch = canvas[y][x]
            if ch == "■":
                line += FULL_CELL_COLOR + "  " + RESET_COLOR
            elif ch == "█":
                line += WALL_COLOR + "  " + RESET_COLOR
            else:
                line += "  "
        print(line)


def main() -> None:

    maze_hex = [
    ["9","5","1","5","3","9","1","5","3","9","5","5","1","7","9","5","1","5","1","1","5","1","1","5","3"],
    ["E","B","A","B","A","E","8","1","2","8","5","3","C","1","4","1","2","B","A","8","1","2","8","1","2"],
    ["9","6","A","8","4","1","6","A","8","4","5","4","5","4","1","2","A","C","4","2","8","2","C","2","A"],
    ["C","3","A","8","3","8","1","6","A","9","3","9","5","3","8","4","4","5","3","A","8","2","D","0","2"],
    ["9","6","8","4","2","A","8","5","2","A","C","0","7","A","A","D","1","3","A","8","2","8","3","C","2"],
    ["C","1","2","9","6","C","4","3","A","A","B","8","3","A","A","9","2","A","A","8","6","8","6","B","A"],
    ["9","2","E","8","5","3","9","6","8","4","2","8","4","4","4","6","8","2","A","C","1","2","9","0","2"],
    ["A","C","3","8","1","4","4","5","2","F","A","8","3","F","F","F","8","2","C","5","2","C","4","2","A"],
    ["8","5","6","8","4","1","1","7","A","F","C","6","8","5","7","F","A","C","1","3","8","3","D","0","6"],
    ["C","5","3","A","D","0","4","3","A","F","F","F","A","F","F","F","8","5","6","A","A","8","1","4","3"],
    ["9","1","4","4","1","2","9","4","2","9","7","F","A","F","D","5","0","1","1","4","2","C","6","B","A"],
    ["A","A","9","1","2","A","C","3","8","4","3","F","A","F","F","F","8","2","8","5","6","D","5","2","A"],
    ["8","4","2","A","8","6","9","2","A","9","2","B","8","5","1","7","C","4","4","5","1","5","5","2","A"],
    ["8","1","6","A","C","3","8","4","4","6","8","2","8","5","2","9","3","9","1","7","A","9","5","4","2"],
    ["C","4","1","6","9","2","8","5","1","3","C","4","4","3","A","8","2","8","4","5","6","C","3","B","A"],
    ["9","1","4","1","6","A","A","9","2","C","3","9","3","A","8","2","8","0","1","5","5","3","A","A","A"],
    ["A","8","1","2","9","2","A","A","8","1","4","6","8","2","C","6","A","8","6","9","3","C","6","A","A"],
    ["A","8","4","4","2","C","6","C","2","C","1","1","6","8","5","5","2","C","1","6","A","9","5","4","2"],
    ["8","6","9","5","6","9","5","1","6","9","2","C","1","4","5","5","4","1","6","9","2","8","5","5","2"],
    ["C","5","4","5","5","4","5","4","5","6","C","5","4","5","5","5","5","4","5","4","4","4","5","5","6"],
]

    H = len(maze_hex)
    W = len(maze_hex[0])

    canvas_height = 2 * H + 1
    canvas_width = 2 * W + 1

    # Colors (ANSI)
    WALL_COLOR = "\033[41m"       # Red
    FULL_CELL_COLOR = "\033[44m"  # Blue
    RESET_COLOR = "\033[0m"

    # Initialize canvas
    canvas = [[" " for _ in range(canvas_width)] for _ in range(canvas_height)]

    # Fill walls and cells
    for r in range(H):
        for c in range(W):
            cell = int(maze_hex[r][c], 16)
            y, x = 2*r + 1, 2*c + 1

            # Use special symbol for fully enclosed cell
            if cell == 0xF:
                canvas[y][x] = "■"  # special symbol
            else:
                canvas[y][x] = " "  # center

            # Wall bits
            north = bool(cell & 1)
            east  = bool(cell & 2)
            south = bool(cell & 4)
            west  = bool(cell & 8)

            # Fill direct walls
            if north: canvas[y-1][x] = "█"
            if south: canvas[y+1][x] = "█"
            if east:  canvas[y][x+1] = "█"
            if west:  canvas[y][x-1] = "█"

            # Junctions if any wall touches corner
            if north or west:   canvas[y-1][x-1] = "█"
            if north or east:   canvas[y-1][x+1] = "█"
            if south or west:   canvas[y+1][x-1] = "█"
            if south or east:   canvas[y+1][x+1] = "█"

    # Outer walls
    for i in range(canvas_height):
        canvas[i][0] = "█"
        canvas[i][-1] = "█"
    for j in range(canvas_width):
        canvas[0][j] = "█"
        canvas[-1][j] = "█"

    # View size (adjust independently)
    VIEW_HEIGHT = 100
    VIEW_WIDTH  = 100

    # Camera position (move these to pan around)
    cam_y = 0
    cam_x = 0

    if VIEW_HEIGHT > canvas_height:
        VIEW_HEIGHT = canvas_height
    if VIEW_WIDTH > canvas_width:
        VIEW_WIDTH = canvas_width

    print_section(
        canvas,
        cam_y,
        cam_x,
        VIEW_HEIGHT,
        VIEW_WIDTH,
        WALL_COLOR,
        FULL_CELL_COLOR,
        RESET_COLOR
    )


if  __name__ == "__main__":
    main()