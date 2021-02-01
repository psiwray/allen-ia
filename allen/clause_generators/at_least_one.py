from typing import List

from allen.clause import Clause
from allen.input.time_intervals_table import TimeIntervalsGroup
from allen.literal import Literal


def generate_at_least_one(group: TimeIntervalsGroup) -> List[Clause]:
    clauses: List[Clause] = []

    for intervals_relationships in group.intervals_relationships:
        clause: Clause = []
        for relationship in intervals_relationships.relationships:
            clause.append(Literal(
                intervals_relationships.t1,
                intervals_relationships.t2,
                relationship))
        clauses.append(clause)

    return clauses
