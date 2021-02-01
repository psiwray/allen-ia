from allen.literal import Literal


class ExpressionLiteral:
    l1: Literal
    l2: Literal
    negated: bool

    def __init__(self, l1: Literal, l2: Literal, negated: bool = False):
        self.l1 = l1
        self.l2 = l2
        self.negated = negated

    def __str__(self):
        return f"{chr(0xAC) if self.negated else ''}[({self.l1}) \u2227 ({str(self.l2)})]"
