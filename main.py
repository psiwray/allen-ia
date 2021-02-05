from allen.input.inverse_relationships_table import read_inverse_relationships_table
from allen.input.ternary_constraints_table import read_ternary_constraints_table
from allen.input.time_intervals_table import read_time_intervals_table
from allen.output.sat_output import generate_sat_output, Data, Coding

if __name__ == "__main__":
    data = Data(
        read_inverse_relationships_table("data/inverse_relationships_table.txt"),
        read_ternary_constraints_table("data/ternary_constraints_table.txt")
    )
    for group in read_time_intervals_table("data/time_intervals/3.txt"):
        print(f"Clauses for group at index {group.number}:")
        for line in generate_sat_output(group, data, Coding.TERNARY_IMPLICATION):
            print(line)
