"""Cell representation for the maze."""

from dataclasses import dataclass


@dataclass
class Cell:
    """Represent a single maze cell."""

    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True
    visited: bool = False
