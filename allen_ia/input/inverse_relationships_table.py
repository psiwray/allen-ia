from re import compile
from typing import List, Dict

from allen_ia.relationship import Relationship


class InverseRelationship:
    """
    Associate the inverse of a relationship to the relationship itself.
    """

    relationship: Relationship
    inverse: Relationship

    def __init__(self, relationship: Relationship, inverse: Relationship):
        self.relationship = relationship
        self.inverse = inverse


# The inverse relationships table is just a list of inverse relationships.
InverseRelationshipsTable = List[InverseRelationship]


def read_inverse_relationships_table(file_path: str) -> InverseRelationshipsTable:
    """
    This function reads the inverse relationships table from a file.

    :param file_path: the file path where to read from.
    :return: the constructed structure.
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
    """
    Convert the inverse relationships table to a simple dictionary where the key is the starting relationship an the
    value is its inverse.

    :param table: the table to convert.
    :return: the constructed dictionary.
    """
    return {i.relationship: i.inverse for i in table}
