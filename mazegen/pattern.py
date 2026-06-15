"""Utilities for placing the required 42 pattern in a maze."""

from mazegen.cell import Cell

PATTERN_42: list[str] = [
    "4 4 222",
    "4 4   2",
    "444 222",
    "  4 2 ",
    "  4 222",
]

PATTERN_WIDTH = 7
PATTERN_HEIGHT = 5
MIN_WIDTH_FOR_PATTERN = 11
MIN_HEIGHT_FOR_PATTERN = 9


def can_draw_pattern(width: int, height: int) -> bool:
    """Return whether the maze is large enough for the 42 pattern."""
    return width >= MIN_WIDTH_FOR_PATTERN and height >= MIN_HEIGHT_FOR_PATTERN


def get_pattern_start(width: int, height: int) -> tuple[int, int]:
    """Return the top-left position used to center the 42 pattern."""
    start_x = (width - PATTERN_WIDTH) // 2
    start_y = (height - PATTERN_HEIGHT) // 2
    return start_x, start_y


def build_pattern_cells(width: int, height: int) -> set[tuple[int, int]]:
    """Build the set of maze cells that draw the 42 pattern."""
    pattern_cells: set[tuple[int, int]] = set()

    if not can_draw_pattern(width, height):
        return pattern_cells

    start_x, start_y = get_pattern_start(width, height)

    for y_offset, row in enumerate(PATTERN_42):
        for x_offset, char in enumerate(row):
            if char != " ":
                x = start_x + x_offset
                y = start_y + y_offset
                pattern_cells.add((x, y))

    return pattern_cells


def reserve_pattern_cells(
    maze: list[list[Cell]],
    pattern_cells: set[tuple[int, int]],
) -> None:
    """Reserve pattern cells by marking them as already visited."""
    for x, y in pattern_cells:
        maze[y][x].visited = True
