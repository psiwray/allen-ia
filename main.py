from allen.clause import clause_to_string, generate_at_least_one, generate_inverse_implication, generate_at_most_one, \
    generate_ternary_implication
from allen.input.inverse_relationships_table import read_inverse_relationships_table
from allen.input.ternary_constraints_table import read_ternary_constraints_table
from allen.input.time_intervals_table import read_time_intervals_table

if __name__ == "__main__":
    inverse_relationships_table = read_inverse_relationships_table("data/inverse_relationships_table.txt")
    ternary_constraints_table = read_ternary_constraints_table("data/ternary_constraints_table.txt")
    time_intervals_table = read_time_intervals_table("data/time_intervals/debug.txt")

    for clause in generate_inverse_implication(time_intervals_table[0], inverse_relationships_table):
        print(clause_to_string(clause))
    print()

    for clause in generate_at_least_one(time_intervals_table[0]):
        print(clause_to_string(clause))
    print()

    for clause in generate_at_most_one(time_intervals_table[0]):
        print(clause_to_string(clause))
    print()

    for clause in generate_ternary_implication(time_intervals_table[0], ternary_constraints_table):
        print(clause_to_string(clause))
    print()
