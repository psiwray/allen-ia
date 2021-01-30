from typing import Dict, List
from re import compile

from relationship import Relationship


class TernaryConstraintsTable:
    constraints: Dict[Relationship, Dict[Relationship, List[Relationship]]]

    def __init__(self):
        self.constraints = {}

    def add_constraint(self, rel1: Relationship, rel2: Relationship, result: List[Relationship]):
        if rel1 not in self.constraints:
            self.constraints[rel1] = {}

        self.constraints[rel1][rel2] = result

    def get_constraint(self, rel1: Relationship, rel2: Relationship):
        return self.constraints[rel1][rel2]


def read(file_path: str) -> TernaryConstraintsTable:
    line_validator = compile(r"(?P<rel1>[^\s]+)\s*:\s*(?P<rel2>[^\s]+)\s*::\s*\(\s*(?P<result>.+)\s*\)")
    ternary_constraints_table = TernaryConstraintsTable()

    with open(file_path, "r") as file:

        for line in file:
            line = line.strip()
            # Skip empty lines.
            if not len(line):
                continue

            def parse_result_string(string: str) -> List[Relationship]:
                matcher = compile(r"[^\s]+\s+")
                matches: List[Relationship] = []
                matches_regex = matcher.findall(string)
                for match_regex in matches_regex:
                    matches.append(Relationship(match_regex.strip()))

                return matches

            match = line_validator.match(line)
            if match:
                ternary_constraints_table.add_constraint(
                    Relationship(match.group("rel1")),
                    Relationship(match.group("rel2")),
                    parse_result_string(match.group("result"))
                )
            else:
                raise RuntimeError("Invalid line found in the ternary constraints table.", line)

    return ternary_constraints_table
