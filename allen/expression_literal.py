from typing import Tuple

from allen.literal import Literal
from allen.relationship import Relationship


class ExpressionLiteral:
    """
    A data structure to collect all the information required to represent an expression literal. In this case, the two
    originating simple literals and an optional negation are what's necessary.
    """
    l1: Literal
    l2: Literal
    negated: bool

    def __init__(self, l1: Literal, l2: Literal, negated: bool = False):
        self.l1 = l1
        self.l2 = l2
        self.negated = negated

    def __str__(self):
        return f"{chr(0xAC) if self.negated else ''}[({self.l1}) \u2227 ({str(self.l2)})]"

    def as_tuple(self) -> Tuple[int, int, Relationship, int, int, Relationship]:
        """
        Convert this literal's data into a tuple that will be used by the output generator to uniquely identify this
        literal across various boolean clauses.

        :return: the tuple.
        """
        return \
            self.l1.t1, self.l1.t2, self.l1.relationship, \
            self.l2.t1, self.l2.t2, self.l2.relationship
