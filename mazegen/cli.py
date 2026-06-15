"""Interactive command-line interface for A-Maze-ing."""

from mazegen.bonus_pattern_color import PATTERN_COLORS
from mazegen.config import load_config, MazeConfig
from mazegen.generator import MazeGenerator
from mazegen.output import write_maze_output
from mazegen.pathfinding import find_shortest_path
from mazegen.render import render_maze

WALL_COLORS = [
    "\033[37m",  # White
    "\033[38;2;255;215;0m",  # Gold
    "\033[38;2;138;43;226m",  # Violet
]


def print_commands(has_pattern: bool) -> None:
    """Print available interactive commands."""
    print("\nCommands:")
    print("[p] Toggle shortest path")
    print("[r] Regenerate maze")
    print("[c] Change wall colour")
    if has_pattern:
        print("[t] Change 42 pattern colour")
    print("[q] Quit")


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
    should_render = True

    while True:
        if should_render:
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
            should_render = False

        print_commands(bool(generator.pattern_42))

        try:
            command = input("> ").strip().lower().lstrip("\ufeff")
        except EOFError:
            print()
            break

        if command == "q":
            break
        elif command == "p":
            show_path = not show_path
            should_render = True
        elif command == "r":
            generator, path = generate_maze_data(config)
            should_render = True
        elif command == "c":
            wall_color_index = (
                wall_color_index + 1
            ) % len(WALL_COLORS)
            should_render = True
        elif command == "t":
            if generator.pattern_42:
                pattern_color_index = (
                    pattern_color_index + 1
                ) % len(PATTERN_COLORS)
                should_render = True
            else:
                print("No 42 pattern is available in this maze.")
        elif command:
            print(f"Unknown command: {command}")
