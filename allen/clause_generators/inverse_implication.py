from typing import List

from allen.clause import Clause
from allen.input.inverse_relationships_table import InverseRelationshipsTable, inverse_relationships_to_dict
from allen.input.time_intervals_table import TimeIntervalsGroup
from allen.literal import Literal
from allen.relationship import Relationship


def generate_inverse_implication(group: TimeIntervalsGroup, table: InverseRelationshipsTable) -> List[Clause]:
    """
    Generate the clauses using the inverse implication algorithm.

    :param group: the time intervals group to execute the algorithm on.
    :param table: the inverse relationships table.
    :return: the generated clauses.
    """

    clauses: List[Clause] = []
    inverse_of = inverse_relationships_to_dict(table)

    # Now build the clauses.
    for intervals_relationships in group.intervals_relationships:
        for relationship in intervals_relationships.relationships:
            # FIXME: Skip the equal relationship since it always generates a true value.
            if relationship == Relationship.EQUAL:
                continue

            clauses.append([
                Literal(
                    intervals_relationships.t1,
                    intervals_relationships.t2,
                    relationship, True
                ),
                Literal(
                    intervals_relationships.t2,
                    intervals_relationships.t1,
                    inverse_of[relationship]
                )
            ])
            clauses.append([
                Literal(
                    intervals_relationships.t2,
                    intervals_relationships.t1,
                    inverse_of[relationship], True
                ),
                Literal(
                    intervals_relationships.t1,
                    intervals_relationships.t2,
                    relationship
                )
            ])

    return clauses
