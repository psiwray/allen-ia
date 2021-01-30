from enum import Enum
from typing import Optional


class Relationship(Enum):
    BEFORE = "<"
    AFTER = ">"
    MEETS = "m"
    MEETS_INVERSE = "mi"
    OVERLAPS = "o"
    OVERLAPS_INVERSE = "oi"
    STARTS = "s"
    STARTS_INVERSE = "si"
    DURING = "d"
    DURING_INVERSE = "di"
    FINISHES = "f"
    FINISHES_INVERSE = "fi"
    EQUAL = "="


def parse(symbol: str) -> Optional[Relationship]:
    try:
        return Relationship(symbol)
    except ValueError:
        return None
