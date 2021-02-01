from allen.relationship import Relationship


class Literal:
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
