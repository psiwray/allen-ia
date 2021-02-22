from typing import List

from allen.clause import Clause
from allen.expression_literal import ExpressionLiteral
from allen.input.ternary_constraints_table import TernaryConstraintsTable, ternary_constraints_to_dict
from allen.input.time_intervals_table import TimeIntervalsGroup, time_intervals_to_dict
from allen.literal import Literal


def generate_expression_reference(group: TimeIntervalsGroup, table: TernaryConstraintsTable) -> List[Clause]:
    """
    Generate the clauses using the expression reference algorithm.

    :param group: the time intervals group to execute the algorithm on.
    :param table: the ternary constraints table.
    :return: the generated clauses.
    """

    clauses: List[Clause] = []

    def generate_clause_for_triple(t1: int, t2: int, t3: int) -> List[Clause]:
        """
        Generate the required clauses for a simple triple.

        :param t1: the first chosen time interval.
        :param t2: the second chosen time interval.
        :param t3: the third chosen time interval.
        :return: the generated clauses.
        """
        generated_clauses: List[Clause] = []
        relationships_dict = ternary_constraints_to_dict(table)
        intervals_dict = time_intervals_to_dict(group)

        t1_t2_relationships = intervals_dict[(t1, t2)]
        t2_t3_relationships = intervals_dict[(t2, t3)]

        for r_t1_t2 in t1_t2_relationships:
            for r_t2_t3 in t2_t3_relationships:
                t1_t3_relationships = relationships_dict[(r_t1_t2, r_t2_t3)]

                for r_t1_t3 in t1_t3_relationships:
                    left_right_implication: Clause = []
                    right_left_implication_1: Clause = []
                    right_left_implication_2: Clause = []

                    # Use a proposition that demonstrates the implication from the left to right.
                    left_right_implication.append(Literal(t2, t3, r_t2_t3, True))
                    left_right_implication.append(Literal(t1, t3, r_t1_t3, True))
                    left_right_implication.append(ExpressionLiteral(
                        Literal(t2, t3, r_t2_t3),
                        Literal(t1, t3, r_t1_t3)
                    ))

                    # Use a proposition that demonstrates the implication from the right to left.
                    right_left_implication_1.append(Literal(t2, t3, r_t2_t3))
                    right_left_implication_1.append(ExpressionLiteral(
                        Literal(t2, t3, r_t2_t3),
                        Literal(t1, t3, r_t1_t3),
                        True
                    ))

                    right_left_implication_2.append(Literal(t1, t3, r_t1_t3))
                    right_left_implication_2.append(ExpressionLiteral(
                        Literal(t2, t3, r_t2_t3),
                        Literal(t1, t3, r_t1_t3),
                        True
                    ))

                    generated_clauses.append(left_right_implication)
                    generated_clauses.append(right_left_implication_1)
                    generated_clauses.append(right_left_implication_2)

                # Add the clause we wanted to generate in the first place using
                # the previously generated expression literals.
                clause: Clause = [Literal(t1, t2, r_t1_t2, True)]
                for r in t1_t3_relationships:
                    clause.append(ExpressionLiteral(
                        Literal(t2, t3, r_t2_t3),
                        Literal(t1, t3, r)
                    ))

                generated_clauses.append(clause)

        return generated_clauses

    n = group.total_time_intervals
    # FIXME: I'm skipping duplicates using a particular set of ranges here.
    #  Specifically, j always starts from i + 1 and k always starts from j + 1.
    #  This means that no duplicates are generated like (0, 0, 1) or even
    #  (0, 0, 0) and at the same time no duplicate clauses (one the opposite of
    #  the other) aren't generated either.
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                clauses.extend(generate_clause_for_triple(i, j, k))

    return clauses
