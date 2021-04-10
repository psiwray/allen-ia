from enum import Enum
from typing import List, Tuple

from allen_ia.clause import Clause, clause_to_string
from allen_ia.clause_generators.at_least_one import generate_at_least_one
from allen_ia.clause_generators.at_most_one import generate_at_most_one
from allen_ia.clause_generators.expression_reference import generate_expression_reference
from allen_ia.clause_generators.inverse_implication import generate_inverse_implication
from allen_ia.clause_generators.ternary_implication import generate_ternary_implication
from allen_ia.expression_literal import ExpressionLiteral
from allen_ia.input.inverse_relationships_table import InverseRelationshipsTable
from allen_ia.input.ternary_constraints_table import TernaryConstraintsTable
from allen_ia.input.time_intervals_table import TimeIntervalsGroup
from allen_ia.literal import Literal
from allen_ia.output.number_dict import NumberDict


class Data:
    """
    A collection of all the data required by the algorithms to generate the clauses.
    """

    def __init__(self, inverse_implications: InverseRelationshipsTable, ternary_constraints: TernaryConstraintsTable):
        self.inverse_implications = inverse_implications
        self.ternary_constraints = ternary_constraints


class Coding(Enum):
    """
    The coding of choice selected by the user.
    """

    TERNARY_IMPLICATION = 0
    EXPRESSION_REFERENCE = 1


class GenerationResult:
    number_dict: NumberDict
    number_lines: List[str]
    math_lines: List[str]
    clauses: List[Clause]

    def __init__(self, number_dict: NumberDict, number_lines: List[str], math_lines: List[str], clauses: List[Clause]):
        self.number_dict = number_dict
        self.number_lines = number_lines
        self.math_lines = math_lines
        self.clauses = clauses


def generate_sat_output_for_group(group: TimeIntervalsGroup, data: Data, coding: Coding = Coding.TERNARY_IMPLICATION) \
        -> GenerationResult:
    """
    First compute the required algorithms on the input data to generate the boolean clauses, then convert those clauses
    into a textual format using the output generator and return.

    :param group: the input data used by the algorithms.
    :param data: the literal identifier generators.
    :param coding: the coding that the user chose.
    :return: the list of generated clauses as strings compatible with SAT input.
    """

    number_dict = NumberDict()
    number_lines: List[str] = []
    math_lines: List[str] = []
    clauses: List[Clause] = []

    # Execute every algorithm on the same set of time intervals.
    last_length = len(clauses)

    clauses.extend(generate_inverse_implication(group, data.inverse_implications))
    print(f"  Inverse implication generated {len(clauses) - last_length} new clauses.")
    last_length = len(clauses)

    clauses.extend(generate_at_least_one(group))
    print(f"  At least one generated {len(clauses) - last_length} new clauses.")
    last_length = len(clauses)

    clauses.extend(generate_at_most_one(group))
    print(f"  At most one generated {len(clauses) - last_length} new clauses.")
    last_length = len(clauses)

    if coding == Coding.TERNARY_IMPLICATION:
        clauses.extend(generate_ternary_implication(group, data.ternary_constraints, data.inverse_implications))
        print(f"  Ternary constraints implication generated {len(clauses) - last_length} new clauses.")
    elif coding == Coding.EXPRESSION_REFERENCE:
        clauses.extend(generate_expression_reference(group, data.ternary_constraints, data.inverse_implications))
        print(f"  Expression reference generated {len(clauses) - last_length} new clauses.")

    print(f"  A total of {len(clauses)} clauses have been generated.")

    # Generate unique identifiers for every literal and add the result to the global list.
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
        math_lines.append(clause_to_string(clause))

    print(f"  A total of {number_dict.get_current_number() - 1} literals have been used.")

    return GenerationResult(number_dict, number_lines, math_lines, clauses)
