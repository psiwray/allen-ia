from allen.clause import clause_to_string
from allen.clause_generators.at_least_one import generate_at_least_one
from allen.clause_generators.at_most_one import generate_at_most_one
from allen.clause_generators.inverse_implication import generate_inverse_implication
from allen.clause_generators.ternary_implication import generate_ternary_implication
from allen.input.inverse_relationships_table import read_inverse_relationships_table
from allen.input.ternary_constraints_table import read_ternary_constraints_table
from allen.input.time_intervals_table import read_time_intervals_table

if __name__ == "__main__":
    inverse_relationships_table = read_inverse_relationships_table("data/inverse_relationships_table.txt")
    ternary_constraints_table = read_ternary_constraints_table("data/ternary_constraints_table.txt")
    time_intervals_table = read_time_intervals_table("data/time_intervals/3.txt")

    print("Inverse implication:")
    for clause in generate_inverse_implication(time_intervals_table[0], inverse_relationships_table):
        print(clause_to_string(clause))

    print("At least one:")
    for clause in generate_at_least_one(time_intervals_table[0]):
        print(clause_to_string(clause))

    print("At most one:")
    for clause in generate_at_most_one(time_intervals_table[0]):
        print(clause_to_string(clause))

    print("Ternary constraints implication:")
    for clause in generate_ternary_implication(time_intervals_table[0], ternary_constraints_table):
        print(clause_to_string(clause))
