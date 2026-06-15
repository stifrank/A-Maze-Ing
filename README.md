*This project has been created as part of the 42 curriculum by fjaramil, digonza2.*

# A-Maze-ing

## Description

A-Maze-ing is a Python maze generator and visualizer developed as part of the 42 curriculum. The program reads a configuration file, generates a maze (perfect or imperfect), writes it to an output file using hexadecimal wall encoding, and displays it interactively in the terminal with ASCII art.

The project is structured as a modular application with a reusable maze generation library (`mazegen`) that can be installed independently via `pip`.

Key features:
- Perfect maze generation (exactly one path between any two cells)
- Imperfect maze generation (multiple paths, cycles)
- Reproducible generation via seed
- Hidden "42" pattern embedded in the maze walls
- Bonus: selectable DFS or Prim generation algorithm
- BFS-based shortest path solver
- Interactive terminal interface (toggle path, change colors, regenerate)
- Bonus: dedicated colour control for the "42" pattern
- Hexadecimal output file with path solution

---

## Instructions

### Requirements

- Python 3.10 or later
- `pip` or another package manager

### Installation

```bash
make install
```

This installs all required dependencies.

### Running the program

```bash
make run
```

Or directly:

```bash
python3 a_maze_ing.py config.txt
```

Where `config.txt` is your configuration file (see format below).

### Other Makefile targets

```bash
make debug       # Run with Python's pdb debugger
make lint        # Run flake8 and mypy checks
make lint-strict # Run mypy with --strict flag
make clean       # Remove __pycache__, .mypy_cache and build artifacts
```

### Building the mazegen package

```bash
make build
```

This generates a `.whl` file at the project root, installable via:

```bash
pip install mazegen-*.whl
```

---

## Configuration file format

The configuration file uses `KEY=VALUE` pairs, one per line. Lines starting with `#` are comments and are ignored.

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Maze width in cells (integer > 0) | `WIDTH=20` |
| `HEIGHT` | Maze height in cells (integer > 0) | `HEIGHT=15` |
| `ENTRY` | Entry cell coordinates as x,y | `ENTRY=0,0` |
| `EXIT` | Exit cell coordinates as x,y | `EXIT=19,14` |
| `OUTPUT_FILE` | Path to the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Whether the maze is perfect | `PERFECT=True` |
| `ALGORITHM` | Optional algorithm: `DFS` or `PRIM` | `ALGORITHM=DFS` |
| `SEED` | Optional integer seed for reproducibility | `SEED=42` |

Example `config.txt`:

```
# A-Maze-ing default configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
ALGORITHM=DFS

# Optional seed for reproducible generation.
# SEED=42
```

---

## Maze generation algorithm

We chose **Depth-First Search (DFS) with iterative backtracking**, also known as the recursive backtracker algorithm.

### How it works

1. Start from the entry cell, mark it as visited.
2. Randomly pick an unvisited neighbor, remove the wall between them, and move to it.
3. If no unvisited neighbors exist, backtrack to the previous cell.
4. Repeat until all cells have been visited.

The result is always a **perfect maze** (a spanning tree): exactly one path exists between any two cells.

### Why DFS

- It produces mazes with long, winding corridors and relatively few dead ends, which are visually interesting and challenging to solve.
- It is simple to implement iteratively with a stack, avoiding Python's recursion limit.
- It naturally guarantees full connectivity with no isolated cells.
- It is well-suited for embedding the "42" pattern by pre-marking those cells as visited before generation starts — the DFS simply routes around them.

For `PERFECT=False`, after the selected perfect algorithm we remove a random subset of internal walls (avoiding the 42 pattern and ensuring no 3×3 open areas are created), introducing cycles and multiple valid paths.

### Bonus: Prim algorithm

As a bonus, the config accepts `ALGORITHM=PRIM`. The Prim implementation lives in `mazegen/bonus_prim.py` so the bonus logic stays clearly separated from the mandatory DFS generator. It grows the maze from the entry cell by repeatedly picking a random frontier wall that reaches an unvisited cell.

DFS remains the default because it is the mandatory, simple baseline. Prim gives a different maze texture while still producing a perfect maze before optional imperfect wall removals.

### Bonus: 42 pattern colour

The terminal renderer also includes a small visual bonus: the "42" pattern can use its own colour, independent from wall colours. The bonus colour list lives in `mazegen/bonus_pattern_color.py`, and the interactive CLI exposes it with the `t` command.

---

## Reusable module

The `mazegen` package exposes the maze generation logic as a standalone, importable library with no dependency on the main program.

### Installation

```bash
pip install mazegen-*.whl
```

### Basic usage

```python
from mazegen import MazeGenerator, MazeConfig

config = MazeConfig(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    output_file="maze.txt",
    perfect=True,
    seed=42,
    algorithm="DFS",
)

generator = MazeGenerator(config)
generator.generate()

# Access the maze grid (list of lists of Cell objects)
maze = generator.maze

# Access the 42 pattern cell positions
pattern = generator.pattern_42
```

### Passing custom parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Number of columns |
| `height` | `int` | Number of rows |
| `entry` | `tuple[int, int]` | Entry cell as (x, y) |
| `exit` | `tuple[int, int]` | Exit cell as (x, y) |
| `output_file` | `str` | Output filename |
| `perfect` | `bool` | Perfect maze if True |
| `seed` | `int \| None` | Seed for reproducibility |
| `algorithm` | `str` | Generation algorithm: `DFS` or bonus `PRIM` |

### Accessing the solution

```python
from mazegen import MazeGenerator, MazeConfig
from mazegen.pathfinding import find_shortest_path

config = MazeConfig(
    width=10, height=10,
    entry=(0, 0), exit=(9, 9),
    output_file="maze.txt",
    perfect=True,
    algorithm="DFS",
)

generator = MazeGenerator(config)
generator.generate()

path = find_shortest_path(generator.maze, config.entry, config.exit)
print("Solution:", "".join(path))  # e.g. "SSEENNESSS..."
```

The maze structure is a `list[list[Cell]]` where each `Cell` has boolean attributes `north`, `east`, `south`, `west` (True = wall present) and `visited`.

---

## Resources

### Algorithm references

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Depth-first search — Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [Spanning tree — Wikipedia](https://en.wikipedia.org/wiki/Spanning_tree)
- [Breadth-first search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Think Labyrinth: Maze algorithms](http://www.astrolog.org/labyrnth/algrithm.htm)

### Python references

- [Python `random` module](https://docs.python.org/3/library/random.html)
- [Python `dataclasses`](https://docs.python.org/3/library/dataclasses.html)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)
- [Python packaging guide](https://packaging.python.org/en/latest/)

### AI usage

AI tools (Claude, ChatGPT) were used during this project for the following tasks:

- Reviewing and debugging the maze generation logic, particularly the 3×3 open area constraint in imperfect mode.
- Improving error handling and type hints across all modules.
- Drafting and structuring this README.
- Suggesting edge cases to test (seed=0, entry/exit at corners, small mazes without room for the 42 pattern).

All AI-generated content was reviewed, tested, and understood before being included in the project.

---

## Team and project management

### Roles

- **fjaramil**: maze generation algorithm (DFS, imperfect mode, 42 pattern), configuration parsing, output file format.
- **digonza2**: terminal rendering, pathfinding (BFS), interactive CLI, packaging and Makefile.

### Planning

Our initial plan was to split the project into two parallel tracks: core generation logic and visual/output layer. This worked well in practice — the `Cell` and `MazeConfig` data structures served as a clear contract between both parts.

The main adjustment during development was adding the 3×3 open area constraint for imperfect mazes, which was not anticipated in the initial plan and required revisiting the generation logic.

### What worked well

- Separating the reusable `mazegen` module from the main program early on made testing and packaging straightforward.
- Using `dataclasses` for `Cell` and `MazeConfig` kept the code clean and type-safe.
- The DFS algorithm was easy to reason about and debug visually.

### What could be improved

- The imperfect mode could offer more control over the density of added cycles.
- Additional bonus algorithms could be added in their own files following the same structure as `bonus_prim.py`.

### Tools used

- Python 3.10+
- `mypy` for static type checking
- `flake8` for code style
- `build` for packaging
- Claude and ChatGPT for code review and debugging assistance
