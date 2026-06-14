"""Reusable maze generation logic."""

import random

from mazegen.cell import Cell
from mazegen.config import MazeConfig


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


class MazeGenerator:
    """Generate and store a maze."""

    def __init__(self, config: MazeConfig) -> None:
        """Initialize the maze generator."""
        self.config: MazeConfig = config
        self.maze: list[list[Cell]] = self._create_grid()
        self.pattern_42: set[tuple[int, int]] = set()

        if self.config.seed is not None:
            random.seed(self.config.seed)

    def _create_grid(self) -> list[list[Cell]]:
        """Create a grid filled with closed cells."""
        return [
            [Cell() for _ in range(self.config.width)]
            for _ in range(self.config.height)
        ]

    def _build_42_pattern(self) -> None:
        """Reserve fully closed cells to draw the 42 pattern."""
        if (
            self.config.width < MIN_WIDTH_FOR_PATTERN
            or self.config.height < MIN_HEIGHT_FOR_PATTERN
        ):
            print("Error: maze too small to draw 42 pattern")
            return

        start_x = (self.config.width - PATTERN_WIDTH) // 2
        start_y = (self.config.height - PATTERN_HEIGHT) // 2

        for y_offset, row in enumerate(PATTERN_42):
            for x_offset, char in enumerate(row):
                if char != " ":
                    x = start_x + x_offset
                    y = start_y + y_offset
                    self.pattern_42.add((x, y))
                    self.maze[y][x].visited = True

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
        self._build_42_pattern()

        start_x, start_y = self.config.entry

        if (start_x, start_y) in self.pattern_42:
            raise ValueError("ENTRY cannot be inside the 42 pattern")

        if self.config.exit in self.pattern_42:
            raise ValueError("EXIT cannot be inside the 42 pattern")

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
