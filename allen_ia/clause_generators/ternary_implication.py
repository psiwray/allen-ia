from typing import List, Optional

from allen_ia.clause import Clause
from allen_ia.clause_generators.generator import Dicts, generate
from allen_ia.input.inverse_relationships_table import InverseRelationshipsTable
from allen_ia.input.ternary_constraints_table import TernaryConstraintsTable
from allen_ia.input.time_intervals_table import TimeIntervalsGroup
from allen_ia.literal import Literal
from allen_ia.relationship import Relationship


def generate_ternary_implication(group: TimeIntervalsGroup, table: TernaryConstraintsTable,
                                 inverse_table: InverseRelationshipsTable) -> List[Clause]:
    """
    Generate the clauses using the ternary implication algorithm.

    :param group: the time intervals group to execute the algorithm on.
    :param table: the ternary constraints table.
    :param inverse_table: the inverse relationships table.
    :return: the generated clauses.
    """

    def generate_clause_for_triplet(dicts: Dicts, t1: int, t2: int, t3: int) -> Optional[List[Clause]]:
        generated_clauses: List[Clause] = []

        t1_t2_relationships: List[Relationship] = dicts.intervals_dict[(t1, t2)]
        t2_t3_relationships: List[Relationship] = dicts.intervals_dict[(t2, t3)]

        for r_t1_t2 in t1_t2_relationships:
            for r_t2_t3 in t2_t3_relationships:
                t1_t3_relationships: List[Relationship] = dicts.relationships_dict[(r_t1_t2, r_t2_t3)]
                clause_for_triplet: Clause = [
                    Literal(t1, t2, r_t1_t2, True),
                    Literal(t2, t3, r_t2_t3, True)
                ]

                added_at_least_something = False
                for r in t1_t3_relationships:
                    # Before adding the relationship to the list we first need to check if it's actually possible for
                    # the first and third time interval to have that relationship. If not, we skip adding this one.
                    if ((t1, t3) in dicts.intervals_dict) and (r in dicts.intervals_dict[(t1, t3)]):
                        clause_for_triplet.append(Literal(t1, t3, r))
                        added_at_least_something = True

                if added_at_least_something:
                    generated_clauses.append(clause_for_triplet)

        return generated_clauses

    for item in generate(group, table, inverse_table, generate_clause_for_triplet):
        yield item
