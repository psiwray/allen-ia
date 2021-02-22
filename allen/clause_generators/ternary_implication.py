from typing import List

from allen.clause import Clause
from allen.input.ternary_constraints_table import TernaryConstraintsTable, ternary_constraints_to_dict
from allen.input.time_intervals_table import TimeIntervalsGroup, time_intervals_to_dict
from allen.literal import Literal
from allen.relationship import Relationship


def generate_ternary_implication(group: TimeIntervalsGroup, table: TernaryConstraintsTable) -> List[Clause]:
    """
    Generate the clauses using the ternary implication algorithm.

    :param group: the time intervals group to execute the algorithm on.
    :param table: the ternary constraints table.
    :return: the generated clauses.
    """

    clauses: List[Clause] = []

    def generate_clause_for_triplet(t1: int, t2: int, t3: int) -> List[Clause]:
        generated_clauses: List[Clause] = []
        relationships_dict = ternary_constraints_to_dict(table)
        intervals_dict = time_intervals_to_dict(group)

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
                    clause_for_triplet.append(Literal(t1, t3, r))

                generated_clauses.append(clause_for_triplet)

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
                clauses.extend(generate_clause_for_triplet(i, j, k))

    return clauses
