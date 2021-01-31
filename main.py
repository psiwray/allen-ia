from input.inverse_relationships_table import read_inverse_relationships_table
from input.ternary_constraints_table import read_ternary_constraints_table
from input.time_intervals_table import read_time_intervals_table

if __name__ == "__main__":
    # print(read_inverse_relationships_table("data/inverse_relationships_table.txt"))
    # print(read_ternary_constraints_table("data/ternary_constraints_table.txt"))

    time_intervals_table = read_time_intervals_table("data/time_intervals_table.txt")
    print(time_intervals_table)
