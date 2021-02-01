from typing import List

from allen.literal import Literal

Clause = List[Literal]


def clause_to_string(clause: Clause) -> str:
    return " \u2228 ".join([str(literal) for literal in clause])
