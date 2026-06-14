"""Output formatting for maze files."""

from mazegen.cell import Cell


def cell_to_hex(cell: Cell) -> str:
    """Convert a cell wall state to one hexadecimal digit."""
    value = 0

    if cell.north:
        value += 1
    if cell.east:
        value += 2
    if cell.south:
        value += 4
    if cell.west:
        value += 8

    return format(value, "X")


def maze_to_hex_lines(maze: list[list[Cell]]) -> list[str]:
    """Convert a maze grid to hexadecimal text lines."""
    lines: list[str] = []

    for row in maze:
        line = ""

        for cell in row:
            line += cell_to_hex(cell)

        lines.append(line)

    return lines


def write_maze_output(
    filename: str,
    maze: list[list[Cell]],
    entry: tuple[int, int],
    exit: tuple[int, int],
    path: list[str],
) -> None:
    """Write the complete maze output to a file."""
    hex_lines = maze_to_hex_lines(maze)

    with open(filename, "w", encoding="utf-8") as file:
        for line in hex_lines:
            file.write(f"{line}\n")

        file.write("\n")

        file.write(f"{entry[0]},{entry[1]}\n")
        file.write(f"{exit[0]},{exit[1]}\n")
        file.write(f"{''.join(path)}\n")
