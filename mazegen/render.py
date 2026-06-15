"""ASCII rendering for mazes."""

from mazegen.cell import Cell

RESET_COLOR = "\033[0m"


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
    width = len(maze[0])
    path_positions = build_path_positions(entry, path)

    for y in range(height):
        top_line = ""
        middle_line = ""

        for x in range(width):
            cell = maze[y][x]
            position = (x, y)

            top_line += color_wall("+", wall_color, True)

            if cell.north:
                top_line += color_wall("---", wall_color, True)
            else:
                top_line += "   "

            if cell.west:
                middle_line += color_wall("|", wall_color, True)
            else:
                middle_line += " "

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
            middle_line += f" {content} "

        top_line += color_wall("+", wall_color, True)

        last_cell = maze[y][width - 1]
        if last_cell.east:
            middle_line += color_wall("|", wall_color, True)
        else:
            middle_line += " "

        lines.append(top_line)
        lines.append(middle_line)

    bottom_line = ""

    for x in range(width):
        bottom_line += color_wall("+", wall_color, True)

        if maze[height - 1][x].south:
            bottom_line += color_wall("---", wall_color, True)
        else:
            bottom_line += "   "

    bottom_line += color_wall("+", wall_color, True)
    lines.append(bottom_line)

    return "\n".join(lines)
