from re import compile
from typing import List

from relationship import Relationship


class TimeIntervalsRelationships:
    t1: int
    t2: int
    relationships: List[Relationship]

    def __init__(self, t1: int, t2: int, relationships: List[Relationship]):
        self.t1 = t1
        self.t2 = t2
        self.relationships = relationships


class TimeIntervalsGroup:
    number: int
    total_time_intervals: int
    intervals_relationships: List[TimeIntervalsRelationships]

    def __init__(self, number: int, total_time_intervals: int,
                 intervals_relationships: List[TimeIntervalsRelationships]):
        self.number = number
        self.total_time_intervals = total_time_intervals
        self.intervals_relationships = intervals_relationships


TimeIntervalsTable = List[TimeIntervalsGroup]


def read_time_intervals_table(file_path: str) -> TimeIntervalsTable:
    time_intervals_groups: TimeIntervalsTable = []
    group_counter: int = 0
    reading_time_intervals = False

    with open(file_path, "r") as file:
        total_time_intervals_regex = compile(r"(?P<count>\d+)\s*")
        time_interval_regex = compile(r"(?P<t1>\d+)\s+(?P<t2>\d+)\s+\(\s*(?P<relationships>.+)\s*\)")

        total_time_intervals = 0
        time_intervals_relationships: List[TimeIntervalsRelationships] = []

        def parse_relationships_string(string: str) -> List[Relationship]:
            matcher = compile(r"[^\s]+")
            matches: List[Relationship] = []
            matches_regex = matcher.findall(string)
            for match_regex in matches_regex:
                matches.append(Relationship(match_regex.strip()))

            return matches

        for line in file:
            # Skip empty lines.
            line = line.strip()
            if not len(line):
                continue

            if reading_time_intervals:
                if line == ".":
                    # This is the end of the current group, make one and add it to the list.
                    time_intervals_groups.append(
                        TimeIntervalsGroup(group_counter, total_time_intervals, time_intervals_relationships))
                    group_counter += 1
                    time_intervals_relationships = []
                    reading_time_intervals = False
                else:
                    # Interpret the line.
                    match = time_interval_regex.match(line)
                    if match:
                        time_intervals_relationships.append(TimeIntervalsRelationships(
                            int(match.group("t1")),
                            int(match.group("t2")),
                            parse_relationships_string(match.group("relationships"))
                        ))
                    else:
                        raise RuntimeError("Invalid time intervals relationships string.", line)
            else:
                # First line is always the number of total time intervals contained.
                match = total_time_intervals_regex.match(line)
                if match:
                    total_time_intervals = int(match.group("count"))
                    reading_time_intervals = True
                else:
                    raise RuntimeError("Failed to fetch total time intervals.")

    return time_intervals_groups
