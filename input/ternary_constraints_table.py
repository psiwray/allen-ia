from re import compile
from typing import List

from relationship import Relationship


class TernaryConstraint:
    relationship_t1_t2: Relationship
    relationship_t2_t3: Relationship
    relationships_t1_t3: List[Relationship]

    def __init__(self, relationship_t1_t2: Relationship, relationship_t2_t3: Relationship,
                 relationships_t1_t3: List[Relationship]):
        self.relationship_t1_t2 = relationship_t1_t2
        self.relationship_t2_t3 = relationship_t2_t3
        self.relationships_t1_t3 = relationships_t1_t3


TernaryConstraintsTable = List[TernaryConstraint]


def read_ternary_constraints_table(file_path: str) -> TernaryConstraintsTable:
    """
    Read the contents of a ternary constraints table and return a structure
    that describes said table.
    :param file_path: the path on disk of the table.
    :return: the constructed table itself.
    """

    line_validator = compile(r"(?P<r1>[^\s]+)\s*:\s*(?P<r2>[^\s]+)\s*::\s*\(\s*(?P<relationships>.+)\s*\)")
    ternary_constraints_table = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            # Skip empty lines.
            if not len(line):
                continue

            def parse_result_string(string: str) -> List[Relationship]:
                matcher = compile(r"[^\s]+")
                matches: List[Relationship] = []
                matches_regex = matcher.findall(string)
                for match_regex in matches_regex:
                    matches.append(Relationship(match_regex.strip()))

                return matches

            match = line_validator.match(line)
            if match:
                ternary_constraints_table.append(TernaryConstraint(
                    Relationship(match.group("r1")),
                    Relationship(match.group("r2")),
                    parse_result_string(match.group("relationships"))
                ))
            else:
                raise RuntimeError("Invalid line found in the ternary constraints table.", line)

    return ternary_constraints_table
