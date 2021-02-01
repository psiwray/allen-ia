from re import compile
from typing import List, Dict

from allen.relationship import Relationship


class InverseRelationship:
    relationship: Relationship
    inverse: Relationship

    def __init__(self, relationship: Relationship, inverse: Relationship):
        self.relationship = relationship
        self.inverse = inverse


InverseRelationshipsTable = List[InverseRelationship]


def read_inverse_relationships_table(file_path: str) -> InverseRelationshipsTable:
    """
    Read the contents of an inverse relationships table and return a structure
    that describes said table.
    :param file_path: the path on disk of the table.
    :return: the constructed table itself.
    """

    line_validator = compile(r"(?P<rel>[^\s]+)\s*::\s*(?P<inverse>[^\s]+)")
    inverse_relationships_table = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            # Skip empty lines.
            if not len(line):
                continue

            # If a match is found, insert the inverse relationship into the structure.
            match = line_validator.match(line)
            if match:
                inverse_relationships_table.append(InverseRelationship(
                    Relationship(match.group("rel")),
                    Relationship(match.group("inverse"))
                ))
            else:
                raise RuntimeError("Invalid line found in the inverse relationships table.", line)

    return inverse_relationships_table


def inverse_relationships_to_dict(table: InverseRelationshipsTable) -> Dict[Relationship, Relationship]:
    return {i.relationship: i.inverse for i in table}
