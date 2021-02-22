from getopt import getopt
from sys import argv
from typing import Optional
from os import mkdir

from allen.input.inverse_relationships_table import read_inverse_relationships_table
from allen.input.ternary_constraints_table import read_ternary_constraints_table
from allen.input.time_intervals_table import read_time_intervals_table
from allen.output.sat_output import generate_sat_output_for_group, Data, Coding

if __name__ == "__main__":
    matched_args, remaining_args = getopt(argv[1:], "d:c:o:", ["data=", "coding=", "output="])


    def find_argument(short: str, long: str) -> Optional[str]:
        for arg_name, arg_value in matched_args:
            if arg_name == short or arg_name == long:
                return arg_value

        return None


    # Parse the arguments from the command-line input.
    data_folder = find_argument("-d", "--data") or "."
    coding = find_argument("-c", "--coding") or "ternary_impl"
    output_folder = find_argument("-o", "--output") or "."
    input_file = remaining_args[0]

    # Read the data from the
    data = Data(
        read_inverse_relationships_table(f"{data_folder}/inverse_relationships_table.txt"),
        read_ternary_constraints_table(f"{data_folder}/ternary_constraints_table.txt")
    )

    # Choose the preferred coding, if specified else choose a default one.
    coding_enum = ""
    if coding == "ternary_impl":
        coding_enum = Coding.TERNARY_IMPLICATION
    elif coding == "expression_ref":
        coding_enum = Coding.EXPRESSION_REFERENCE

    # Write the result to files, one for every group.
    for group in read_time_intervals_table(input_file):
        try:
            mkdir(output_folder)
        except FileExistsError:
            pass

        with open(f"{output_folder}/{group.number}.txt", "w") as file:
            for line in generate_sat_output_for_group(group, data, coding_enum):
                file.write(line)
                file.write("\n")
