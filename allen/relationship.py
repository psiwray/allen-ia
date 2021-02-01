from enum import Enum


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

    def __str__(self):
        return f"{self.value}"
