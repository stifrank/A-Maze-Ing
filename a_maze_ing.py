"""Main entry point for A-Maze-ing."""

import sys

from mazegen.config import load_config
from mazegen.generator import MazeGenerator
from mazegen.output import maze_to_hex_lines


def main() -> None:
    """Run the program."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    try:
        config = load_config(sys.argv[1])
        generator = MazeGenerator(config)
        generator.generate()
        lines = maze_to_hex_lines(generator.maze)

        print("Configuration loaded successfully")
        print(f"Width: {config.width}")
        print(f"Height: {config.height}")
        print(f"Rows created: {len(generator.maze)}")
        print(f"Cells per row: {len(generator.maze[0])}")
        print("Maze generated successfully")
        print(generator.maze[0][0])
        print(generator.maze[0][1])
        for line in lines:
            print(line)

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
