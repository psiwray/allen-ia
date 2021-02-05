from enum import Enum
from typing import List

from allen.clause import Clause
from allen.clause_generators.at_least_one import generate_at_least_one
from allen.clause_generators.at_most_one import generate_at_most_one
from allen.clause_generators.expression_reference import generate_expression_reference
from allen.clause_generators.inverse_implication import generate_inverse_implication
from allen.clause_generators.ternary_implication import generate_ternary_implication
from allen.expression_literal import ExpressionLiteral
from allen.input.inverse_relationships_table import InverseRelationshipsTable
from allen.input.ternary_constraints_table import TernaryConstraintsTable
from allen.input.time_intervals_table import TimeIntervalsGroup
from allen.literal import Literal
from allen.output.number_dict import NumberDict


class Data:
    def __init__(self, inverse_implications: InverseRelationshipsTable, ternary_constraints: TernaryConstraintsTable):
        self.inverse_implications = inverse_implications
        self.ternary_constraints = ternary_constraints


class Coding(Enum):
    TERNARY_IMPLICATION = 0
    EXPRESSION_REFERENCE = 1


def generate_sat_output(group: TimeIntervalsGroup, data: Data, coding: Coding = Coding.TERNARY_IMPLICATION):
    number_dict = NumberDict()
    number_lines: List[str] = []
    clauses: List[Clause] = []

    clauses.extend(generate_inverse_implication(group, data.inverse_implications))
    clauses.extend(generate_at_least_one(group))
    clauses.extend(generate_at_most_one(group))
    if coding == Coding.TERNARY_IMPLICATION:
        clauses.extend(generate_ternary_implication(group, data.ternary_constraints))
        # print("Using the ternary implication coding.")
    elif coding == Coding.EXPRESSION_REFERENCE:
        # print("Using the expression reference coding.")
        clauses.extend(generate_expression_reference(group, data.ternary_constraints))

    for clause in clauses:
        number_line: List[int] = []
        number: int = 0

        for literal in clause:
            if isinstance(literal, Literal):
                if number_dict.is_literal_identified(literal):
                    number = number_dict.get_literal_number(literal)
                else:
                    number = number_dict.register_literal(literal)
            elif isinstance(literal, ExpressionLiteral):
                if number_dict.is_expression_literal_identified(literal):
                    number = number_dict.get_expression_literal_identifier(literal)
                else:
                    number = number_dict.register_expression_literal(literal)

            if literal.negated:
                number = -number

            number_line.append(number)

        number_line.append(0)
        number_lines.append(" ".join([str(n) for n in number_line]))

    return number_lines
