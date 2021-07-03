from typing import List, Optional

from allen_ia.clause import Clause
from allen_ia.clause_generators.generator import Dicts, generate
from allen_ia.expression_literal import ExpressionLiteral
from allen_ia.input.inverse_relationships_table import InverseRelationshipsTable
from allen_ia.input.ternary_constraints_table import TernaryConstraintsTable
from allen_ia.input.time_intervals_table import TimeIntervalsGroup
from allen_ia.literal import Literal


def generate_expression_reference(group: TimeIntervalsGroup, table: TernaryConstraintsTable,
                                  inverse_table: InverseRelationshipsTable) -> List[Clause]:
    """
    Generate the clauses using the expression reference algorithm.

    :param group: the time intervals group to execute the algorithm on.
    :param table: the ternary constraints table.
    :param inverse_table: the inverse relationships table.
    :return: the generated clauses.
    """

    def generate_clause_for_triplet(dicts: Dicts, t1: int, t2: int, t3: int) -> Optional[List[Clause]]:
        generated_clauses: List[Clause] = []

        t1_t2_relationships = dicts.intervals_dict[(t1, t2)]
        t2_t3_relationships = dicts.intervals_dict[(t2, t3)]

        for r_t1_t2 in t1_t2_relationships:
            clause: Clause = [Literal(t1, t2, r_t1_t2, True)]
            for r_t2_t3 in t2_t3_relationships:
                t1_t3_relationships = dicts.relationships_dict[(r_t1_t2, r_t2_t3)]

                for r_t1_t3 in t1_t3_relationships:
                    left_right_implication: Clause = []
                    right_left_implication_1: Clause = []
                    right_left_implication_2: Clause = []

                    # Use a proposition that demonstrates the implication from left to right.
                    left_right_implication.append(Literal(t2, t3, r_t2_t3, True))
                    left_right_implication.append(Literal(t1, t3, r_t1_t3, True))
                    left_right_implication.append(ExpressionLiteral(
                        Literal(t2, t3, r_t2_t3),
                        Literal(t1, t3, r_t1_t3)
                    ))

                    # Use a proposition that demonstrates the implication from right to left.
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

                    # Add all generated clauses to the master list.
                    generated_clauses.append(left_right_implication)
                    generated_clauses.append(right_left_implication_1)
                    generated_clauses.append(right_left_implication_2)

                # Add the clause we wanted to generate in the first place using
                # the previously generated expression literals.
                for r in t1_t3_relationships:
                    if ((t1, t3) in dicts.intervals_dict) and (r in dicts.intervals_dict[(t1, t3)]):
                        clause.append(ExpressionLiteral(
                            Literal(t2, t3, r_t2_t3),
                            Literal(t1, t3, r)
                        ))

            generated_clauses.append(clause)

        return generated_clauses

    for item in generate(group, table, inverse_table, generate_clause_for_triplet):
        yield item
