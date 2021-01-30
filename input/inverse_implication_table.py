from re import compile
from typing import Dict

from relationship import Relationship


class InverseRelationshipsTable:
    """
    With this table we are representing the inverse of a specific relationship.
    For example, if we have the "before" relationship, its inverse would be
    "after"; if we have "overlaps with" then its inverse would be "is overlapped
    by".
    """

    relationships: Dict[Relationship, Relationship]

    def __init__(self):
        self.relationships = {}

    def add_inverse(self, rel: Relationship, inverse: Relationship):
        """
        Add a new inverse relationship to a given relationship.
        :param rel: the relationship we want to add its inverse to.
        :param inverse: the inverse relationship.
        """
        self.relationships[rel] = inverse

    def get_inverse_of(self, rel: Relationship):
        """
        Get the inverse of a given relationship.
        :param rel: the relationship we want to get the inverse of.
        :return: the inverse relationship.
        """
        return self.relationships[rel]

    def __getitem__(self, item: Relationship):
        return self.get_inverse_of(item)


def read(file_path: str) -> InverseRelationshipsTable:
    """
    Read the contents of an inverse relationships table and return a structure
    that describes said table.
    :param file_path: the path on disk of the table.
    :return: the constructed table itself.
    """

    line_validator = compile(r"\s*(?P<rel>[^\s]+)\s*::\s*(?P<inverse>[^\s]+)\s*")
    inverse_relationships_table = InverseRelationshipsTable()

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            # Skip empty lines.
            if not len(line):
                continue

            # If a match is found, insert the inverse relationship into the structure.
            match = line_validator.match(line)
            if match:
                inverse_relationships_table.add_inverse(
                    Relationship(match.group("rel")),
                    Relationship(match.group("inverse"))
                )
            else:
                raise RuntimeError("Invalid line found in the inverse relationships table.", line)

    return inverse_relationships_table
