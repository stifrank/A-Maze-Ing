"""Bonus: randomized Prim maze generation algorithm."""

import random

from mazegen.cell import Cell
from mazegen.config import MazeConfig


def get_frontier_edges(
    config: MazeConfig,
    maze: list[list[Cell]],
    x: int,
    y: int,
) -> list[tuple[int, int, str]]:
    """Return frontier wall edges that lead to unvisited neighbors."""
    edges: list[tuple[int, int, str]] = []
    directions: list[tuple[int, int, str]] = [
        (0, -1, "N"),
        (1, 0, "E"),
        (0, 1, "S"),
        (-1, 0, "W"),
    ]

    for dx, dy, direction in directions:
        next_x = x + dx
        next_y = y + dy

        if (
            0 <= next_x < config.width
            and 0 <= next_y < config.height
            and not maze[next_y][next_x].visited
        ):
            edges.append((x, y, direction))

    return edges


def remove_wall(
    maze: list[list[Cell]],
    x: int,
    y: int,
    direction: str,
) -> None:
    """Remove the wall between a cell and its selected neighbor."""
    current = maze[y][x]

    if direction == "N":
        current.north = False
        maze[y - 1][x].south = False
    elif direction == "E":
        current.east = False
        maze[y][x + 1].west = False
    elif direction == "S":
        current.south = False
        maze[y + 1][x].north = False
    elif direction == "W":
        current.west = False
        maze[y][x - 1].east = False


def target_position(x: int, y: int, direction: str) -> tuple[int, int]:
    """Return the position reached from a cell in the given direction."""
    if direction == "N":
        return x, y - 1
    if direction == "E":
        return x + 1, y
    if direction == "S":
        return x, y + 1
    return x - 1, y


def add_frontier(
    config: MazeConfig,
    maze: list[list[Cell]],
    frontier: list[tuple[int, int, str]],
    x: int,
    y: int,
) -> None:
    """Add all unvisited neighbor edges of a cell to the frontier."""
    frontier.extend(get_frontier_edges(config, maze, x, y))


def generate_prim(config: MazeConfig, maze: list[list[Cell]]) -> None:
    """Generate a perfect maze using randomized Prim's algorithm.

    This is a bonus algorithm. It grows the maze from the entry cell by
    repeatedly choosing a random frontier wall that reaches an unvisited cell.
    """
    start_x, start_y = config.entry
    maze[start_y][start_x].visited = True

    frontier: list[tuple[int, int, str]] = []
    add_frontier(config, maze, frontier, start_x, start_y)

    while frontier:
        index = random.randrange(len(frontier))
        x, y, direction = frontier.pop(index)
        next_x, next_y = target_position(x, y, direction)

        if maze[next_y][next_x].visited:
            continue

        remove_wall(maze, x, y, direction)
        maze[next_y][next_x].visited = True
        add_frontier(config, maze, frontier, next_x, next_y)
