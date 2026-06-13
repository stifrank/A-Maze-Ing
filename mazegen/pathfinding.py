"""Pathfinding utilities for mazes."""

from collections import deque

from mazegen.cell import Cell


def get_accessible_neighbors(
    maze: list[list[Cell]],
    x: int,
    y: int,
) -> list[tuple[int, int, str]]:
    """Return neighbors reachable from the current cell."""
    neighbors: list[tuple[int, int, str]] = []
    cell = maze[y][x]

    if not cell.north:
        neighbors.append((x, y - 1, "N"))
    if not cell.east:
        neighbors.append((x + 1, y, "E"))
    if not cell.south:
        neighbors.append((x, y + 1, "S"))
    if not cell.west:
        neighbors.append((x - 1, y, "W"))

    return neighbors


def find_shortest_path(
    maze: list[list[Cell]],
    start: tuple[int, int],
    end: tuple[int, int],
) -> list[str]:
    """Find the shortest path between two cells using BFS."""
    queue: deque[tuple[int, int]] = deque([start])
    visited: set[tuple[int, int]] = {start}
    parents: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}

    while queue:
        x, y = queue.popleft()

        if (x, y) == end:
            break

        for next_x, next_y, direction in get_accessible_neighbors(maze, x, y):
            next_position = (next_x, next_y)

            if next_position not in visited:
                visited.add(next_position)
                parents[next_position] = ((x, y), direction)
                queue.append(next_position)

    if end not in visited:
        return []

    path: list[str] = []
    current = end

    while current != start:
        previous, direction = parents[current]
        path.append(direction)
        current = previous

    path.reverse()
    return path
