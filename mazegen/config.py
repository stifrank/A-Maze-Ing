"""Configuration loading and validation for A-Maze-ing."""

from dataclasses import dataclass


REQUIRED_KEYS: set[str] = {
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
}


@dataclass
class MazeConfig:
    """Validated maze configuration."""

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None
    algorithm: str = "DFS"


def parse_positive_int(value: str, key: str) -> int:
    """Parse a strictly positive integer value."""
    try:
        number = int(value)
    except ValueError as exc:
        raise ValueError(f"{key} must be an integer") from exc
    if number <= 0:
        raise ValueError(f"{key} must be greater than 0")
    return number


def parse_seed(value: str) -> int:
    """Parse a seed value (any integer including 0 is valid)."""
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError("SEED must be an integer") from exc


def parse_bool(value: str) -> bool:
    """Parse a boolean value."""
    normalized_value = value.lower()
    if normalized_value == "true":
        return True
    if normalized_value == "false":
        return False
    raise ValueError("PERFECT must be True or False")


def parse_algorithm(value: str) -> str:
    """Parse the optional maze generation algorithm."""
    algorithm = value.upper()
    if algorithm not in {"DFS", "PRIM"}:
        raise ValueError("ALGORITHM must be DFS or PRIM")
    return algorithm


def parse_coordinates(value: str, key: str) -> tuple[int, int]:
    """Parse coordinates in x,y format."""
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(f"{key} must use x,y format")
    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError as exc:
        raise ValueError(f"{key} coordinates must be integers") from exc
    return x, y


def validate_coordinates(
    point: tuple[int, int],
    key: str,
    width: int,
    height: int,
) -> None:
    """Validate that coordinates are inside maze bounds."""
    x, y = point
    if x < 0 or x >= width or y < 0 or y >= height:
        raise ValueError(f"{key} must be inside maze bounds")


def load_config(path: str) -> MazeConfig:
    """Load and validate a maze configuration file."""
    raw_config: dict[str, str] = {}

    try:
        with open(path, "r", encoding="utf-8") as config_file:
            for line_number, line in enumerate(config_file, start=1):
                stripped_line = line.strip()

                if not stripped_line or stripped_line.startswith("#"):
                    continue

                if "=" not in stripped_line:
                    raise ValueError(
                        f"Invalid syntax at line {line_number}: "
                        "expected KEY=VALUE"
                    )

                key, value = stripped_line.split("=", 1)
                key = key.strip().upper()
                value = value.strip()

                if not key or not value:
                    raise ValueError(
                        f"Invalid syntax at line {line_number}: "
                        "empty key or value"
                    )

                raw_config[key] = value

    except FileNotFoundError as exc:
        raise ValueError(f"Configuration file not found: {path}") from exc

    missing_keys = REQUIRED_KEYS - raw_config.keys()
    if missing_keys:
        missing = ", ".join(sorted(missing_keys))
        raise ValueError(f"Missing required key(s): {missing}")

    width = parse_positive_int(raw_config["WIDTH"], "WIDTH")
    height = parse_positive_int(raw_config["HEIGHT"], "HEIGHT")
    entry = parse_coordinates(raw_config["ENTRY"], "ENTRY")
    exit_point = parse_coordinates(raw_config["EXIT"], "EXIT")
    output_file = raw_config["OUTPUT_FILE"]
    perfect = parse_bool(raw_config["PERFECT"])

    if not output_file:
        raise ValueError("OUTPUT_FILE must not be empty")

    validate_coordinates(entry, "ENTRY", width, height)
    validate_coordinates(exit_point, "EXIT", width, height)

    if entry == exit_point:
        raise ValueError("ENTRY and EXIT must be different")

    seed = None
    if "SEED" in raw_config:
        seed = parse_seed(raw_config["SEED"])

    algorithm = "DFS"
    if "ALGORITHM" in raw_config:
        algorithm = parse_algorithm(raw_config["ALGORITHM"])

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_point,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
        algorithm=algorithm,
    )
