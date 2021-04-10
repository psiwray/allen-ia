from typing import List

from allen_ia.clause import Clause
from allen_ia.input.time_intervals_table import TimeIntervalsGroup
from allen_ia.literal import Literal


def generate_at_most_one(group: TimeIntervalsGroup) -> List[Clause]:
    """
    Generate the clauses using the at most one algorithm.

    :param group: the time intervals group to execute the algorithm on.
    :return: the generated clauses.
    """

    for intervals_relationships in group.intervals_relationships:
        # With this loop duplicates are eliminated.
        for i in range(len(intervals_relationships.relationships)):
            for j in range(i + 1, len(intervals_relationships.relationships)):
                r1 = intervals_relationships.relationships[i]
                r2 = intervals_relationships.relationships[j]

                yield [
                    Literal(
                        intervals_relationships.t1,
                        intervals_relationships.t2,
                        r1, True
                    ),
                    Literal(
                        intervals_relationships.t1,
                        intervals_relationships.t2,
                        r2, True
                    )
                ]
