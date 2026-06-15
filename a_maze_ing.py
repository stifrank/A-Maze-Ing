"""Main entry point for A-Maze-ing."""

import sys

from mazegen.cli import run_cli


def main() -> None:
    """Run the program."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    try:
        run_cli(sys.argv[1])

    except (OSError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
