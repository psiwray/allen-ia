from getopt import getopt
from sys import argv
from typing import Optional, Union
from os import mkdir, linesep

from allen.input.inverse_relationships_table import read_inverse_relationships_table
from allen.input.ternary_constraints_table import read_ternary_constraints_table
from allen.input.time_intervals_table import read_time_intervals_table
from allen.output.sat_output import generate_sat_output_for_group, Data, Coding

if __name__ == "__main__":
    matched_args, remaining_args = getopt(argv[1:], "d:c:o", ["data=", "coding=", "output="])


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
    try:
        mkdir(output_folder)
    except FileExistsError:
        pass

    for group in read_time_intervals_table(input_file):
        output_number, output_math = generate_sat_output_for_group(group, data, coding_enum)
        with open(f"{output_folder}/{group.number}.sat", "w") as file:
            for output in output_number:
                file.write(output)
                file.write(linesep)

        # Also write the corresponding mathematical representation to a separate file, with the same name but
        # having a different extension.
        with open(f"{output_folder}/{group.number}.math", "w") as file:
            for output in output_math:
                file.write(output)
                file.write(linesep)
