from __future__ import annotations

# python built-in imports
from dataclasses import dataclass


@dataclass
class Movie:
    id: str
    title: str
    genres: list[str]
    runtime: int
    release_date: str
    budget: int
    score: float | None
