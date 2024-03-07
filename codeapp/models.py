from __future__ import annotations

# python built-in imports
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Movie:
    id: str
    title: str
    genres: list[str]
    runtime: int
    release_date: date
    budget: int
    score: float