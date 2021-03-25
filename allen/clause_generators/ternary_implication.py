from typing import List

from allen.clause import Clause
from allen.input.inverse_relationships_table import InverseRelationshipsTable, inverse_relationships_to_dict
from allen.input.ternary_constraints_table import TernaryConstraintsTable, ternary_constraints_to_dict
from allen.input.time_intervals_table import TimeIntervalsGroup, time_intervals_to_dict
from allen.literal import Literal
from allen.relationship import Relationship


def generate_ternary_implication(group: TimeIntervalsGroup, table: TernaryConstraintsTable,
                                 inverse_table: InverseRelationshipsTable) -> List[Clause]:
    """
    Generate the clauses using the ternary implication algorithm.

    :param group: the time intervals group to execute the algorithm on.
    :param table: the ternary constraints table.
    :param inverse_table: the inverse relationships table.
    :return: the generated clauses.
    """

    clauses: List[Clause] = []
    inverse_relationships_dict = inverse_relationships_to_dict(inverse_table)
    intervals_dict = time_intervals_to_dict(group)
    relationships_dict = ternary_constraints_to_dict(table)

    # Expand the intervals dictionary to include inverse mappings too.
    intervals_dict_ext = {}
    for (t_from, t_to), relationships in intervals_dict.items():
        intervals_dict_ext[(t_to, t_from)] = [inverse_relationships_dict[r] for r in relationships]
    intervals_dict.update(intervals_dict_ext)

    def generate_clause_for_triplet(t1: int, t2: int, t3: int) -> List[Clause]:
        generated_clauses: List[Clause] = []

        # First find the possible combinations of relationships between (i, j)
        # and (j, k) using the time intervals. Next, check what possible
        # relationships can occur between (i, k) and use them to construct a
        # single clause.
        t1_t2_relationships: List[Relationship] = intervals_dict[(t1, t2)]
        t2_t3_relationships: List[Relationship] = intervals_dict[(t2, t3)]

        for r_t1_t2 in t1_t2_relationships:
            for r_t2_t3 in t2_t3_relationships:
                t1_t3_relationships: List[Relationship] = relationships_dict[(r_t1_t2, r_t2_t3)]
                clause_for_triplet: Clause = [
                    Literal(t1, t2, r_t1_t2, True),
                    Literal(t2, t3, r_t2_t3, True)
                ]

                for r in t1_t3_relationships:
                    # Before adding the relationship to the list we first need to check if it's actually possible for
                    # the first and third time interval to have that relationship. If not, we skip adding this one.
                    if r in intervals_dict[(t1, t3)]:
                        clause_for_triplet.append(Literal(t1, t3, r))
                    # else:
                    #     print(f"Skipped non-existent relationship '{r}' between t{t1} and t{t3}.")

                generated_clauses.append(clause_for_triplet)

        return generated_clauses

    n = group.total_time_intervals
    # for i in range(n):
    #     for j in range(i + 1, n):
    #         for k in range(j + 1, n):
    #             clauses.extend(generate_clause_for_triplet(i, j, k))

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i == j or j == k or i == k:
                    continue
                clauses.extend(generate_clause_for_triplet(i, j, k))

    return clauses
