from re import compile
from typing import List, Tuple, Dict

from allen.relationship import Relationship


class TimeIntervalsRelationships:
    """
    This gathers all possible relationships that can be found between two time intervals.
    """

    t1: int
    t2: int
    relationships: List[Relationship]

    def __init__(self, t1: int, t2: int, relationships: List[Relationship]):
        self.t1 = t1
        self.t2 = t2
        self.relationships = relationships


class TimeIntervalsGroup:
    """
    This describes a single group containing a list of time intervals relationships and the total number of time
    intervals found for the current group. The total time intervals is an integer number that's one more than the
    maximum time interval identifier. Each time interval is also identified by an integer number, starting from zero.
    """

    number: int
    total_time_intervals: int
    intervals_relationships: List[TimeIntervalsRelationships]
    comment: str

    def __init__(self, number: int, total_time_intervals: int,
                 intervals_relationships: List[TimeIntervalsRelationships], comment: str):
        self.number = number
        self.total_time_intervals = total_time_intervals
        self.intervals_relationships = intervals_relationships
        self.comment = comment


# A time intervals table is just a list of time intervals groups.
TimeIntervalsTable = List[TimeIntervalsGroup]


def read_time_intervals_table(file_path: str) -> TimeIntervalsTable:
    """
    This function reads the time intervals table from a file.

    :param file_path: the file path where to read from.
    :return: the constructed structure.
    """

    time_intervals_groups: TimeIntervalsTable = []
    group_counter: int = 0
    reading_time_intervals = False

    with open(file_path, "r") as file:
        # This is basically a simple state machine that keeps track of which point the scanning is currently at. For
        # example, it might need to read a new group and thus parse the header, or read a list of lines or find the end
        # of the current group and so on. Regular expressions are used to quickly match lines.

        total_time_intervals_regex = compile(r"(?P<count>\d+)(?P<comment>.*)\s*")
        time_interval_regex = compile(r"(?P<t1>\d+)\s+(?P<t2>\d+)\s+\(\s*(?P<relationships>.+)\s*\)")

        total_time_intervals = 0
        time_intervals_relationships: List[TimeIntervalsRelationships] = []

        def parse_relationships_string(string: str) -> List[Relationship]:
            """
            This parses a list of relationships written between round brackets.

            :param string: the string to read from.
            :return: the list of relationships found.
            """
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
                    time_intervals_groups.append(TimeIntervalsGroup(
                        group_counter, total_time_intervals,
                        time_intervals_relationships, comment))
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
                    comment = match.group("comment")
                    reading_time_intervals = True
                else:
                    raise RuntimeError("Failed to fetch total time intervals.")

    return time_intervals_groups


def time_intervals_to_dict(group: TimeIntervalsGroup) -> Dict[Tuple[int, int], List[Relationship]]:
    """
    Convert the time intervals group to a simple dictionary where the key is the pair of time intervals identifiers and
    the value is the list of relationships.

    :param group: the group to convert.
    :return: the constructed dictionary.
    """
    return {(i.t1, i.t2): i.relationships for i in group.intervals_relationships}
