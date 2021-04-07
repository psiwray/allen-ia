from getopt import getopt
from random import randint, seed
from sys import argv
from typing import List, Tuple, Dict, Set, Optional

from allen.relationship import Relationship

Interval = Tuple[int, int]
RelationshipBetweenIntervals = Tuple[int, Relationship, int]


def generate_time_intervals(total: int, max_time: int) -> List[Interval]:
    time_intervals: List[Interval] = []

    for i in range(total):
        start = randint(0, max_time - 1)
        end = randint(start + 1, max_time)

        time_intervals.append((start, end))

    return time_intervals


def find_relationships_between_time_intervals(time_intervals: List[Tuple[int, int]]) -> \
        List[RelationshipBetweenIntervals]:
    relationships: List[RelationshipBetweenIntervals] = []

    def find_relationship(t0: Interval, t1: Interval) -> Relationship:
        t0_from = t0[0]
        t0_to = t0[1]
        t1_from = t1[0]
        t1_to = t1[1]

        if t0_from == t1_from and t0_to == t1_to:
            return Relationship.EQUAL
        else:
            if t0_from < t1_from and t0_to < t1_to and t0_to == t1_from:
                return Relationship.MEETS
            elif t1_from < t0_from and t1_to < t0_to and t1_to == t0_from:
                return Relationship.MEETS_INVERSE
            elif t0_from < t1_from and t0_to < t1_to and t1_from < t0_to:
                return Relationship.OVERLAPS
            elif t1_from < t0_from and t1_to < t0_to and t0_from < t1_to:
                return Relationship.OVERLAPS_INVERSE
            elif t0_from < t1_from and t0_to < t1_to:
                return Relationship.BEFORE
            elif t1_from < t0_from and t1_to < t0_to:
                return Relationship.AFTER
            elif t0_from == t1_from and t0_to < t1_to:
                return Relationship.STARTS
            elif t1_from == t0_from and t1_to < t0_to:
                return Relationship.STARTS_INVERSE
            elif t0_from > t1_from and t0_to < t1_to:
                return Relationship.DURING
            elif t1_from > t0_from and t1_to < t0_to:
                return Relationship.DURING_INVERSE
            elif t0_from > t1_from and t0_to == t1_to:
                return Relationship.FINISHES
            elif t1_from > t0_from and t1_to == t0_to:
                return Relationship.FINISHES_INVERSE

    last_time_interval = len(time_intervals)
    for t0 in range(0, last_time_interval - 1):
        for t1 in range(t0 + 1, last_time_interval):
            relationship = find_relationship(time_intervals[t0], time_intervals[t1])
            relationships.append((t0, relationship, t1))

    return relationships


Instance = Dict[Tuple[int, int], Set[Relationship]]


def generate_instance(total_intervals: int, max_time: int, iterations: int) -> Instance:
    instance: Instance = {}

    for i in range(iterations):
        intervals = generate_time_intervals(total_intervals, max_time)
        relationships = find_relationships_between_time_intervals(intervals)

        # Merge the relationships together into the single instance.
        for t_from, relationship, t_to in relationships:
            if (t_from, t_to) in instance:
                existing_relationships = instance[(t_from, t_to)]
                existing_relationships.add(relationship)
                instance[(t_from, t_to)] = existing_relationships
            else:
                new_relationships: Set[Relationship] = set()
                new_relationships.add(relationship)
                instance[(t_from, t_to)] = new_relationships

    return instance


def format_instance(instance: Instance, group: int) -> List[str]:
    lines: List[str] = []

    lines.append(f"{group} # {hex(id(instance))}")
    for (t_from, t_to), relationships in instance.items():
        lines.append(f" {t_from} {t_to} ( {' '.join([r.value for r in relationships])} )")
    lines.append(".")

    return lines


if __name__ == "__main__":
    matched_args, remaining_args = getopt(argv[1:], "t:m:i:g",
                                          ["total-intervals=", "max-time=", "iterations=", "groups="])


    def find_argument(short: str, long: str) -> Optional[str]:
        for arg_name, arg_value in matched_args:
            if arg_name == short or arg_name == long:
                return arg_value

        return None


    # Parse the arguments from the command-line input.
    total_intervals = find_argument("-t", "--total-intervals") or 10
    max_time = find_argument("-m", "--max-time") or 40
    iterations = find_argument("-i", "--iterations") or 5
    groups = find_argument("-g", "--groups") or 10

    seed()
    for i in range(int(groups)):
        instance = generate_instance(int(total_intervals), int(max_time), int(iterations))
        for line in format_instance(instance, i):
            print(line)
        print()
