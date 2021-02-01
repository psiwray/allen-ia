from typing import List, Union

from allen.expression_literal import ExpressionLiteral
from allen.literal import Literal

Clause = List[Union[Literal, ExpressionLiteral]]


def clause_to_string(clause: Clause) -> str:
    return " \u2228 ".join([str(literal) for literal in clause])
