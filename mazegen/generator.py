"""Reusable maze generation logic."""

import random

from mazegen.cell import Cell
from mazegen.config import MazeConfig


class MazeGenerator:
    """Generate and store a maze."""

    def __init__(self, config: MazeConfig) -> None:
        """Initialize the maze generator."""
        self.config: MazeConfig = config
        self.maze: list[list[Cell]] = self._create_grid()

        if self.config.seed is not None:
            random.seed(self.config.seed)

    def _create_grid(self) -> list[list[Cell]]:
        """Create a grid filled with closed cells."""
        return [
            [Cell() for _ in range(self.config.width)]
            for _ in range(self.config.height)
        ]
    
    def _get_unvisited_neighbors(
        self,
        x: int,
        y: int,
    ) -> list[tuple[int, int, str]]:
        """Return unvisited neighbor cells around a position."""
        neighbors: list[tuple[int, int, str]] = []
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
                0 <= next_x < self.config.width
                and 0 <= next_y < self.config.height
                and not self.maze[next_y][next_x].visited
            ):
                neighbors.append((next_x, next_y, direction))

        return neighbors
    
    def _remove_wall(self, x: int, y: int, direction: str) -> None:
        """Remove the wall between the current cell and its neighbor."""
        current = self.maze[y][x]

        if direction == "N":
            current.north = False
            self.maze[y - 1][x].south = False
        elif direction == "E":
            current.east = False
            self.maze[y][x + 1].west = False
        elif direction == "S":
            current.south = False
            self.maze[y + 1][x].north = False
        elif direction == "W":
            current.west = False
            self.maze[y][x - 1].east = False

    def generate(self) -> None:
        """Generate a perfect maze using iterative backtracking."""
        start_x, start_y = self.config.entry
        stack: list[tuple[int, int]] = [(start_x, start_y)]

        self.maze[start_y][start_x].visited = True

        while stack:
            x, y = stack[-1]
            neighbors = self._get_unvisited_neighbors(x, y)

            if neighbors:
                next_x, next_y, direction = random.choice(neighbors)
                self._remove_wall(x, y, direction)
                self.maze[next_y][next_x].visited = True
                stack.append((next_x, next_y))
            else:
                stack.pop()

