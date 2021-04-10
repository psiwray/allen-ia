from enum import Enum


class Relationship(Enum):
    """
    Representation of a relationship. Every enumeration's key also contains the
    symbol used to describe the relationship.
    """

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
