from dataclasses import dataclass
from typing import Any, List


@dataclass
class Rider:
    """Rider data class - individual riders info"""

    name: str
    club: str
    points_df: Any


@dataclass
class RaceField:
    """Race field data class - holds every riders info"""

    field: List[Rider]
