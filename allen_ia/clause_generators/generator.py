from typing import List, Callable, Optional, Tuple, Dict

from allen_ia.clause import Clause
from allen_ia.input.inverse_relationships_table import InverseRelationshipsTable, inverse_relationships_to_dict
from allen_ia.input.ternary_constraints_table import TernaryConstraintsTable, ternary_constraints_to_dict
from allen_ia.input.time_intervals_table import TimeIntervalsGroup, time_intervals_to_dict
from allen_ia.relationship import Relationship


class Dicts:
    inverse_relationships_dict: Dict[Relationship, Relationship]
    intervals_dict: Dict[Tuple[int, int], List[Relationship]]
    relationships_dict: Dict[Tuple[Relationship, Relationship], List[Relationship]]

    def __init__(self, group: TimeIntervalsGroup, table: TernaryConstraintsTable,
                 inverse_table: InverseRelationshipsTable):
        self.inverse_relationships_dict = inverse_relationships_to_dict(inverse_table)
        self.intervals_dict = time_intervals_to_dict(group)
        self.relationships_dict = ternary_constraints_to_dict(table)

        # Expand the intervals dictionary to include inverse mappings too.
        intervals_dict_ext = {}
        for (t_from, t_to), relationships in self.intervals_dict.items():
            intervals_dict_ext[(t_to, t_from)] = [self.inverse_relationships_dict[r] for r in relationships]
        self.intervals_dict.update(intervals_dict_ext)


TripletFunc = Callable[[Dicts, int, int, int], Optional[List[Clause]]]


def generate(group: TimeIntervalsGroup, table: TernaryConstraintsTable,
             inverse_table: InverseRelationshipsTable,
             triplet_func: TripletFunc) -> List[Clause]:
    dicts = Dicts(group, table, inverse_table)
    n = group.total_time_intervals
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i == j or j == k or i == k:
                    continue
                generation_result = triplet_func(dicts, i, j, k)
                if generation_result:
                    for clause in generation_result:
                        yield clause
