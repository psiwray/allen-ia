from typing import List, Union

from allen_ia.expression_literal import ExpressionLiteral
from allen_ia.literal import Literal

# A clause is simply a collection of literals (either simple or expression) ORed together.
Clause = List[Union[Literal, ExpressionLiteral]]


def clause_to_string(clause: Clause) -> str:
    """
    Get the textual representation of this clause in a human-readable format.

    :param clause: the clause to convert.
    :return: the textual format.
    """
    return " \u2228 ".join([str(literal) for literal in clause])
