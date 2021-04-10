from re import compile
from typing import List, Tuple, Dict

from allen_ia.relationship import Relationship


class TernaryConstraint:
    """
    This represents the possible relationships that can occur between two time intervals t1 and t3 if the relationships
    between t1-t2 and t2-t3 are defined.
    """

    relationship_t1_t2: Relationship
    relationship_t2_t3: Relationship
    relationships_t1_t3: List[Relationship]

    def __init__(self, relationship_t1_t2: Relationship, relationship_t2_t3: Relationship,
                 relationships_t1_t3: List[Relationship]):
        self.relationship_t1_t2 = relationship_t1_t2
        self.relationship_t2_t3 = relationship_t2_t3
        self.relationships_t1_t3 = relationships_t1_t3


# The ternary constraints table is simply a list of ternary constraints.
TernaryConstraintsTable = List[TernaryConstraint]


def read_ternary_constraints_table(file_path: str) -> TernaryConstraintsTable:
    """
    This function reads the ternary constraints table from a file.

    :param file_path: the file path where to read from.
    :return: the constructed structure.
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


def ternary_constraints_to_dict(table: TernaryConstraintsTable) -> \
        Dict[Tuple[Relationship, Relationship], List[Relationship]]:
    """
    Convert the ternary constraints table to a simple dictionary where the key is the pair of relationships found
    between t1-t2 and t2-t3 and the value is the possible relationships that can be found between t1-t3.

    :param table: the table to convert.
    :return: the constructed dictionary.
    """
    return {(i.relationship_t1_t2, i.relationship_t2_t3): i.relationships_t1_t3 for i in table}
