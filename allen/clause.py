from typing import List

from allen.input.inverse_relationships_table import InverseRelationshipsTable, inverse_relationships_to_dict
from allen.input.ternary_constraints_table import TernaryConstraintsTable
from allen.input.time_intervals_table import TimeIntervalsGroup
from allen.literal import Literal
from allen.relationship import Relationship

Clause = List[Literal]


def clause_to_string(clause: Clause) -> str:
    return " \u2228 ".join([str(literal) for literal in clause])


def generate_inverse_implication(group: TimeIntervalsGroup, table: InverseRelationshipsTable) -> List[Clause]:
    clauses: List[Clause] = []
    inverse_of = inverse_relationships_to_dict(table)

    # Now build the clauses.
    for intervals_relationships in group.intervals_relationships:
        for relationship in intervals_relationships.relationships:
            # FIXME: Skip the equal relationship since it always generates a true value.
            if relationship == Relationship.EQUAL:
                continue

            clause: Clause = [
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
            ]
            clauses.append(clause)

    return clauses


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


def generate_at_most_one(group: TimeIntervalsGroup) -> List[Clause]:
    clauses: List[Clause] = []

    for intervals_relationships in group.intervals_relationships:
        # FIXME: With this loop duplicates are eliminated.
        for i in range(len(intervals_relationships.relationships)):
            for j in range(i + 1, len(intervals_relationships.relationships)):
                r1 = intervals_relationships.relationships[i]
                r2 = intervals_relationships.relationships[j]

                clauses.append([
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
                ])

    return clauses


def generate_ternary_implication(group: TimeIntervalsGroup, table: TernaryConstraintsTable) -> List[Clause]:
    clauses: List[Clause] = []

    def generate_clause_for_triplet(t1: int, t2: int, t3: int) -> List[Clause]:
        generated_clauses: List[Clause] = []

        # First find the possible combinations of relationships between (i, j)
        # and (j, k) using the time intervals. Next, check what possible
        # relationships can occur between (i, k) and use them to construct a
        # single clause.
        t1_t2_relationships: List[Relationship] = []
        t2_t3_relationships: List[Relationship] = []

        for intervals_relationships in group.intervals_relationships:
            if intervals_relationships.t1 == t1 and intervals_relationships.t2 == t2:
                t1_t2_relationships.extend(intervals_relationships.relationships)
        for intervals_relationships in group.intervals_relationships:
            if intervals_relationships.t1 == t2 and intervals_relationships.t2 == t3:
                t2_t3_relationships.extend(intervals_relationships.relationships)

        for r_t1_t2 in t1_t2_relationships:
            for r_t2_t3 in t2_t3_relationships:
                t1_t3_relationships: List[Relationship] = []
                clause_for_triplet: Clause = []

                for item in table:
                    if item.relationship_t1_t2 == r_t1_t2 and item.relationship_t2_t3 == r_t2_t3:
                        t1_t3_relationships.extend(item.relationships_t1_t3)
                        break

                clause_for_triplet.append(Literal(t1, t2, r_t1_t2, True))
                clause_for_triplet.append(Literal(t2, t3, r_t2_t3, True))

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
