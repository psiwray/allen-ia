import input.inverse_relationships_table
import input.ternary_constraints_table

if __name__ == "__main__":
    irt = input.inverse_relationships_table.read("data/inverse_relationships_table.txt")
    print(irt)
    tct = input.ternary_constraints_table.read("data/ternary_constraints_table.txt")
    print(tct)
