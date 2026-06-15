"""ASCII rendering for mazes."""

from mazegen.cell import Cell

RESET_COLOR = "\033[0m"
ENTRY_COLOR = "\033[92m"
EXIT_COLOR = "\033[91m"


def color_wall(
    text: str,
    wall_color: str,
    should_color: bool,
) -> str:
    """Return wall text with color when needed."""
    if not should_color:
        return text
    return f"{wall_color}{text}{RESET_COLOR}"


def build_path_positions(
    entry: tuple[int, int],
    path: list[str] | None,
) -> set[tuple[int, int]]:
    """Build the set of positions included in the path."""
    positions: set[tuple[int, int]] = set()

    if path is None:
        return positions

    x, y = entry
    positions.add((x, y))

    for direction in path:
        if direction == "N":
            y -= 1
        elif direction == "E":
            x += 1
        elif direction == "S":
            y += 1
        elif direction == "W":
            x -= 1
        positions.add((x, y))

    return positions


def get_cell_content(
    x: int,
    y: int,
    entry: tuple[int, int],
    exit: tuple[int, int],
    pattern_42: set[tuple[int, int]],
    path_positions: set[tuple[int, int]],
) -> str:
    """Return the character displayed inside a cell."""
    position = (x, y)

    if position == entry:
        return "S"
    if position == exit:
        return "E"
    if position in pattern_42:
        return "#"
    if position in path_positions:
        return "."
    return " "


def color_cell_content(
    content: str,
    position: tuple[int, int],
    pattern_42: set[tuple[int, int]],
    pattern_color: str,
) -> str:
    """Apply the bonus 42 pattern colour when available."""
    if position in pattern_42 and pattern_color:
        return f"{pattern_color}{content}{RESET_COLOR}"
    return content


def color_entry_exit_content(
    content: str,
    position: tuple[int, int],
    entry: tuple[int, int],
    exit: tuple[int, int],
) -> str:
    """Apply fixed colours to entry and exit markers."""
    if position == entry:
        return f"{ENTRY_COLOR}{content}{RESET_COLOR}"
    if position == exit:
        return f"{EXIT_COLOR}{content}{RESET_COLOR}"
    return content


def get_pattern_wall_color(
    position: tuple[int, int],
    neighbor: tuple[int, int] | None,
    pattern_42: set[tuple[int, int]],
    wall_color: str,
    pattern_color: str,
) -> str:
    """Return the 42 colour for walls that belong to pattern cells."""
    if not pattern_color:
        return wall_color
    if position in pattern_42:
        return pattern_color
    if neighbor is not None and neighbor in pattern_42:
        return pattern_color
    return wall_color


def get_pattern_corner_color(
    vertex_x: int,
    vertex_y: int,
    pattern_42: set[tuple[int, int]],
    wall_color: str,
    pattern_color: str,
) -> str:
    """Return the 42 colour for corners touching pattern cells."""
    if not pattern_color:
        return wall_color

    touching_cells = [
        (vertex_x - 1, vertex_y - 1),
        (vertex_x, vertex_y - 1),
        (vertex_x - 1, vertex_y),
        (vertex_x, vertex_y),
    ]

    for cell in touching_cells:
        if cell in pattern_42:
            return pattern_color

    return wall_color


def build_top_segment(
    cell: Cell,
    corner_color: str,
    wall_color: str,
) -> str:
    """Build the top wall segment for one rendered cell."""
    segment = color_wall("+", corner_color, True)
    if cell.north:
        segment += color_wall("---", wall_color, True)
    else:
        segment += "   "
    return segment


def build_middle_segment(
    cell: Cell,
    content: str,
    wall_color: str,
) -> str:
    """Build the middle segment for one rendered cell."""
    if cell.west:
        return f"{color_wall('|', wall_color, True)} {content} "
    return f"  {content} "


def get_cell_wall_colors(
    x: int,
    y: int,
    pattern_42: set[tuple[int, int]],
    wall_color: str,
    pattern_color: str,
) -> tuple[str, str, str]:
    """Return top, west and corner colours for a rendered cell."""
    position = (x, y)
    north_neighbor = (x, y - 1) if y > 0 else None
    west_neighbor = (x - 1, y) if x > 0 else None
    top_wall_color = get_pattern_wall_color(
        position,
        north_neighbor,
        pattern_42,
        wall_color,
        pattern_color,
    )
    west_wall_color = get_pattern_wall_color(
        position,
        west_neighbor,
        pattern_42,
        wall_color,
        pattern_color,
    )
    corner_color = get_pattern_corner_color(
        x,
        y,
        pattern_42,
        wall_color,
        pattern_color,
    )

    return top_wall_color, west_wall_color, corner_color


def render_cell_segments(
    maze: list[list[Cell]],
    x: int,
    y: int,
    entry: tuple[int, int],
    exit: tuple[int, int],
    pattern_42: set[tuple[int, int]],
    path_positions: set[tuple[int, int]],
    wall_color: str,
    pattern_color: str,
) -> tuple[str, str]:
    """Render the top and middle segments for one cell."""
    cell = maze[y][x]
    position = (x, y)
    top_wall_color, west_wall_color, corner_color = get_cell_wall_colors(
        x,
        y,
        pattern_42,
        wall_color,
        pattern_color,
    )

    content = get_cell_content(
        x,
        y,
        entry,
        exit,
        pattern_42,
        path_positions,
    )
    content = color_cell_content(
        content,
        position,
        pattern_42,
        pattern_color,
    )
    content = color_entry_exit_content(
        content,
        position,
        entry,
        exit,
    )

    return (
        build_top_segment(cell, corner_color, top_wall_color),
        build_middle_segment(cell, content, west_wall_color),
    )


def build_row_right_border(
    maze: list[list[Cell]],
    y: int,
    pattern_42: set[tuple[int, int]],
    wall_color: str,
    pattern_color: str,
) -> tuple[str, str]:
    """Build the final corner and right border for one rendered row."""
    width = len(maze[0])

    final_corner_color = get_pattern_corner_color(
        width,
        y,
        pattern_42,
        wall_color,
        pattern_color,
    )
    top_segment = color_wall("+", final_corner_color, True)

    last_cell = maze[y][width - 1]
    if last_cell.east:
        east_wall_color = get_pattern_wall_color(
            (width - 1, y),
            None,
            pattern_42,
            wall_color,
            pattern_color,
        )
        return top_segment, color_wall("|", east_wall_color, True)
    return top_segment, " "


def render_row(
    maze: list[list[Cell]],
    y: int,
    entry: tuple[int, int],
    exit: tuple[int, int],
    pattern_42: set[tuple[int, int]],
    path_positions: set[tuple[int, int]],
    wall_color: str,
    pattern_color: str,
) -> tuple[str, str]:
    """Render the top and middle lines for one maze row."""
    top_line = ""
    middle_line = ""

    for x in range(len(maze[0])):
        top_segment, middle_segment = render_cell_segments(
            maze,
            x,
            y,
            entry,
            exit,
            pattern_42,
            path_positions,
            wall_color,
            pattern_color,
        )
        top_line += top_segment
        middle_line += middle_segment

    top_segment, middle_segment = build_row_right_border(
        maze,
        y,
        pattern_42,
        wall_color,
        pattern_color,
    )
    top_line += top_segment
    middle_line += middle_segment

    return top_line, middle_line


def render_bottom_line(
    maze: list[list[Cell]],
    pattern_42: set[tuple[int, int]],
    wall_color: str,
    pattern_color: str,
) -> str:
    """Render the bottom border of the maze."""
    height = len(maze)
    width = len(maze[0])
    bottom_line = ""

    for x in range(width):
        bottom_wall_color = get_pattern_wall_color(
            (x, height - 1),
            None,
            pattern_42,
            wall_color,
            pattern_color,
        )
        bottom_corner_color = get_pattern_corner_color(
            x,
            height,
            pattern_42,
            wall_color,
            pattern_color,
        )
        bottom_line += color_wall("+", bottom_corner_color, True)

        if maze[height - 1][x].south:
            bottom_line += color_wall("---", bottom_wall_color, True)
        else:
            bottom_line += "   "

    final_bottom_corner_color = get_pattern_corner_color(
        width,
        height,
        pattern_42,
        wall_color,
        pattern_color,
    )
    bottom_line += color_wall("+", final_bottom_corner_color, True)
    return bottom_line


def render_maze(
    maze: list[list[Cell]],
    entry: tuple[int, int],
    exit: tuple[int, int],
    pattern_42: set[tuple[int, int]],
    path: list[str] | None = None,
    wall_color: str = "",
    pattern_color: str = "",
) -> str:
    """Render a maze as ASCII text."""
    lines: list[str] = []
    height = len(maze)
    path_positions = build_path_positions(entry, path)

    for y in range(height):
        top_line, middle_line = render_row(
            maze,
            y,
            entry,
            exit,
            pattern_42,
            path_positions,
            wall_color,
            pattern_color,
        )
        lines.append(top_line)
        lines.append(middle_line)

    lines.append(
        render_bottom_line(maze, pattern_42, wall_color, pattern_color)
    )

    return "\n".join(lines)
