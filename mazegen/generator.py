"""Reusable maze generation logic."""

import random

from mazegen.cell import Cell
from mazegen.bonus_prim import generate_prim
from mazegen.config import MazeConfig
from mazegen.pattern import (
    build_pattern_cells,
    can_draw_pattern,
    MIN_HEIGHT_FOR_PATTERN,
    MIN_WIDTH_FOR_PATTERN,
    reserve_pattern_cells,
)

IMPERFECT_WALL_REMOVAL_RATIO = 0.15
ERROR_COLOR = "\033[91m"
RESET_COLOR = "\033[0m"


class MazeGenerator:
    """Generate and store a maze."""

    def __init__(self, config: MazeConfig) -> None:
        """Initialize the maze generator."""
        self.config: MazeConfig = config
        self.maze: list[list[Cell]] = self._create_grid()
        self.pattern_42: set[tuple[int, int]] = set()

        if self.config.seed is not None:
            random.seed(self.config.seed)
        else:
            random.seed(None)

    def _create_grid(self) -> list[list[Cell]]:
        """Create a grid filled with closed cells."""
        return [
            [Cell() for _ in range(self.config.width)]
            for _ in range(self.config.height)
        ]

    def _build_42_pattern(self) -> None:
        """Reserve fully closed cells to draw the 42 pattern."""
        if not can_draw_pattern(self.config.width, self.config.height):
            print(
                f"\n{ERROR_COLOR}"
                "Error: maze too small to draw 42 pattern. "
                f"Minimum size is {MIN_WIDTH_FOR_PATTERN}x"
                f"{MIN_HEIGHT_FOR_PATTERN}. "
                "Continuing without it."
                f"{RESET_COLOR}\n"
            )
            return

        self.pattern_42 = build_pattern_cells(
            self.config.width,
            self.config.height,
        )
        reserve_pattern_cells(self.maze, self.pattern_42)

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

    def _is_3x3_open(self, bx: int, by: int) -> bool:
        """Check if the 3x3 block with top-left at (bx, by) is fully open.

        A 3x3 block is fully open when all 6 internal walls are absent:
        - East walls of columns bx and bx+1 (for rows by, by+1, by+2)
        - South walls of rows by and by+1 (for cols bx, bx+1, bx+2)
        """
        width = self.config.width
        height = self.config.height

        if bx + 2 >= width or by + 2 >= height:
            return False

        # Check all internal east walls (between columns)
        for row in range(by, by + 3):
            for col in range(bx, bx + 2):
                if self.maze[row][col].east:
                    return False

        # Check all internal south walls (between rows)
        for row in range(by, by + 2):
            for col in range(bx, bx + 3):
                if self.maze[row][col].south:
                    return False

        return True

    def _would_create_3x3(self, x: int, y: int, direction: str) -> bool:
        """Return True if removing this wall would create a 3x3 open area.

        Checks all 3x3 blocks that contain the wall being removed.
        Simulates the removal temporarily to test, then restores.
        """
        # Temporarily remove the wall
        self._remove_wall(x, y, direction)

        # Determine which 3x3 blocks could be affected.
        # A wall between (x,y) and its neighbor belongs to blocks
        # whose top-left corner ranges from (x-2, y-2) to (x, y).
        creates_open = False

        if direction == "E":
            # Wall is between (x,y) and (x+1,y): affects blocks in rows
            # [y-2..y] and cols [x-1..x]
            for by in range(max(0, y - 2), y + 1):
                for bx in range(max(0, x - 1), x + 1):
                    if self._is_3x3_open(bx, by):
                        creates_open = True
                        break
                if creates_open:
                    break

        elif direction == "S":
            # Wall is between (x,y) and (x,y+1): affects blocks in rows
            # [y-1..y] and cols [x-2..x]
            for by in range(max(0, y - 1), y + 1):
                for bx in range(max(0, x - 2), x + 1):
                    if self._is_3x3_open(bx, by):
                        creates_open = True
                        break
                if creates_open:
                    break

        # Restore the wall
        if direction == "E":
            self.maze[y][x].east = True
            self.maze[y][x + 1].west = True
        elif direction == "S":
            self.maze[y][x].south = True
            self.maze[y + 1][x].north = True

        return creates_open

    def _generate_perfect(self) -> None:
        """Generate a perfect maze using iterative DFS backtracking."""
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

    def _add_imperfections(self) -> None:
        """Remove extra internal walls to create multiple paths.

        Skips walls adjacent to the 42 pattern and walls that would
        create a 3x3 open area (forbidden by the subject).
        """
        width = self.config.width
        height = self.config.height

        candidates: list[tuple[int, int, str]] = []

        for y in range(height):
            for x in range(width):
                if x + 1 < width:
                    if (x, y) not in self.pattern_42 and (
                        x + 1, y
                    ) not in self.pattern_42:
                        if self.maze[y][x].east:
                            candidates.append((x, y, "E"))

                if y + 1 < height:
                    if (x, y) not in self.pattern_42 and (
                        x, y + 1
                    ) not in self.pattern_42:
                        if self.maze[y][x].south:
                            candidates.append((x, y, "S"))

        random.shuffle(candidates)
        target = max(1, int(len(candidates) * IMPERFECT_WALL_REMOVAL_RATIO))
        removed = 0

        for x, y, direction in candidates:
            if removed >= target:
                break
            if not self._would_create_3x3(x, y, direction):
                self._remove_wall(x, y, direction)
                removed += 1

    def generate(self) -> None:
        """Generate a maze according to the PERFECT configuration flag.

        Always starts with a perfect DFS maze. If PERFECT is False,
        additional walls are removed to create multiple paths between
        entry and exit, while never creating 3x3 open areas.
        """
        self._build_42_pattern()

        if self.config.entry in self.pattern_42:
            raise ValueError("ENTRY cannot be inside the 42 pattern")

        if self.config.exit in self.pattern_42:
            raise ValueError("EXIT cannot be inside the 42 pattern")

        if self.config.algorithm == "PRIM":
            generate_prim(self.config, self.maze)
        else:
            self._generate_perfect()

        if not self.config.perfect:
            self._add_imperfections()
