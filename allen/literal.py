from typing import Tuple

from allen.relationship import Relationship


class Literal:
    """
    A data structure to collect all the information required to represent a simple literal. In this case, the two time
    intervals, the relationship between them and an optional negation are what's necessary to create a literal.
    """

    t1: int
    t2: int
    relationship: Relationship
    negated: bool

    def __init__(self, t1: int, t2: int, relationship: Relationship, negated: bool = False):
        self.t1 = t1
        self.t2 = t2
        self.relationship = relationship
        self.negated = negated

    def __str__(self):
        return f"{chr(0xAC) if self.negated else ''}(t{self.t1} {self.relationship} t{self.t2})"

    def as_tuple(self) -> Tuple[int, int, Relationship]:
        """
        Convert this literal's data into a tuple that will be used by the output generator to uniquely identify this
        literal across various boolean clauses.

        :return: the tuple.
        """
        return self.t1, self.t2, self.relationship
