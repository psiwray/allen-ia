from typing import Dict, Tuple

from allen.expression_literal import ExpressionLiteral
from allen.literal import Literal
from allen.relationship import Relationship


class NumberDict:
    identified_literals: Dict[Tuple[int, int, Relationship], int]
    identified_expression_literals: Dict[Tuple[int, int, Relationship, int, int, Relationship], int]

    _current_number: int

    def __init__(self):
        self.identified_literals = {}
        self.identified_expression_literals = {}

        self._current_number = 1

    def get_literal_number(self, literal: Literal):
        return self.identified_literals[literal.as_tuple()]

    def get_expression_literal_identifier(self, literal: ExpressionLiteral):
        return self.identified_expression_literals[literal.as_tuple()]

    def is_literal_identified(self, literal: Literal):
        return literal.as_tuple() in self.identified_literals

    def is_expression_literal_identified(self, literal: ExpressionLiteral):
        return literal.as_tuple() in self.identified_expression_literals

    def register_literal(self, literal: Literal) -> int:
        old_number = self._current_number
        self.identified_literals[literal.as_tuple()] = self._current_number
        self._current_number += 1
        return old_number

    def register_expression_literal(self, literal: ExpressionLiteral) -> int:
        old_number = self._current_number
        self.identified_expression_literals[literal.as_tuple()] = self._current_number
        self._current_number += 1
        return old_number
