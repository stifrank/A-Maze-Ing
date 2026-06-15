"""Interactive command-line interface for A-Maze-ing."""

from mazegen.bonus_pattern_color import PATTERN_COLORS
from mazegen.config import load_config, MazeConfig
from mazegen.generator import MazeGenerator
from mazegen.output import write_maze_output
from mazegen.pathfinding import find_shortest_path
from mazegen.render import render_maze

WALL_COLORS = [
    "\033[37m",  # White
    "\033[31m",  # Red
    "\033[32m",  # Green
    "\033[34m",  # Blue
]


def generate_maze_data(
    config: MazeConfig,
) -> tuple[MazeGenerator, list[str]]:
    """Generate a maze and its shortest path."""
    generator = MazeGenerator(config)

    generator.generate()

    path = find_shortest_path(
        generator.maze,
        config.entry,
        config.exit,
    )

    write_maze_output(
        config.output_file,
        generator.maze,
        config.entry,
        config.exit,
        path,
    )

    return generator, path


def run_cli(config_path: str) -> None:
    """Run the interactive maze interface."""
    config = load_config(config_path)

    generator, path = generate_maze_data(config)

    show_path = True
    wall_color_index = 0
    pattern_color_index = 0

    while True:
        current_path = path if show_path else None

        print(
            render_maze(
                generator.maze,
                config.entry,
                config.exit,
                generator.pattern_42,
                current_path,
                WALL_COLORS[wall_color_index],
                PATTERN_COLORS[pattern_color_index],
            )
        )

        print("\nCommands:")
        print("[p] Toggle shortest path")
        print("[r] Regenerate maze")
        print("[c] Change wall colour")
        print("[t] Change 42 pattern colour")
        print("[q] Quit")

        try:
            command = input("> ").strip().lower()
        except EOFError:
            print()
            break

        if command == "q":
            break
        elif command == "p":
            show_path = not show_path
        elif command == "r":
            generator, path = generate_maze_data(config)
        elif command == "c":
            wall_color_index = (
                wall_color_index + 1
            ) % len(WALL_COLORS)
        elif command == "t":
            pattern_color_index = (
                pattern_color_index + 1
            ) % len(PATTERN_COLORS)
