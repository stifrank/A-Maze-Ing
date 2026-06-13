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
