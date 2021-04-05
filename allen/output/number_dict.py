from typing import Dict, Tuple, Optional

from allen.expression_literal import ExpressionLiteral
from allen.literal import Literal
from allen.relationship import Relationship


class NumberDict:
    """
    A data structure used to keep track of all the literals that have been found. If a new literal is found, a new
    positive integer identifier is assigned to it and recorded in the data structure, otherwise its identifier is looked
    up and used.

    Tuples are used to uniquely identify literals across clauses and dictionaries are used to associate that information
    with the literal's identifier.
    """

    identified_literals: Dict[Tuple[int, int, Relationship], int]
    identified_expression_literals: Dict[Tuple[int, int, Relationship, int, int, Relationship], int]
    reverse_identified_literals: Dict[int, Literal]
    reverse_identified_expression_literals: Dict[int, ExpressionLiteral]

    # Unique positive integer number used to identify new literals.
    _current_number: int

    def __init__(self):
        self.identified_literals = {}
        self.identified_expression_literals = {}
        self.reverse_identified_literals = {}
        self.reverse_identified_expression_literals = {}

        self._current_number = 1

    def get_literal_number(self, literal: Literal):
        """
        Get the number of an already-identified simple literal.

        :param literal: the literal's data.
        :return: the literal's identifier.
        """
        return self.identified_literals[literal.as_tuple()]

    def get_expression_literal_identifier(self, literal: ExpressionLiteral):
        """
        Get the number of an already-identified expression literal.

        :param literal: the literal's data.
        :return: the literal's identifier.
        """
        return self.identified_expression_literals[literal.as_tuple()]

    def is_literal_identified(self, literal: Literal):
        """
        Is the given simple literal identified yet?

        :param literal: the literal's data.
        :return: the identification status.
        """
        return literal.as_tuple() in self.identified_literals

    def is_expression_literal_identified(self, literal: ExpressionLiteral):
        """
        Is the given expression literal identified yet?

        :param literal: the literal's data.
        :return: the identification status.
        """
        return literal.as_tuple() in self.identified_expression_literals

    def register_literal(self, literal: Literal) -> int:
        """
        Add a new association for a given simple literal.

        :param literal: the literal's data.
        :return: the new identification number for the literal.
        """

        old_number = self._current_number
        self.identified_literals[literal.as_tuple()] = self._current_number
        self.reverse_identified_literals[self._current_number] = literal
        self._current_number += 1
        return old_number

    def register_expression_literal(self, literal: ExpressionLiteral) -> int:
        """
        Add a new association for a given expression literal.

        :param literal: the literal's data.
        :return: the new identification number for the literal.
        """

        old_number = self._current_number
        self.identified_expression_literals[literal.as_tuple()] = self._current_number
        self.reverse_identified_expression_literals[self._current_number] = literal
        self._current_number += 1
        return old_number

    def get_current_number(self):
        return self._current_number

    def get_literal_from_number(self, number: int) -> Optional[Literal]:
        if number in self.reverse_identified_literals:
            return self.reverse_identified_literals[number]
        return None

    def get_expression_literal_from_number(self, number: int) -> Optional[ExpressionLiteral]:
        if number in self.reverse_identified_expression_literals:
            return self.reverse_identified_expression_literals[number]
        return None
