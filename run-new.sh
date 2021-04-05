#!/bin/bash

input_time_intervals=$1
output_folder_root=$2

for sat_input in $input_time_intervals/*.txt; do
  python3 -s main.py --data=data --output=$output_folder_root/ternary_impl/`basename $sat_input` --coding=ternary_impl --solver=/usr/bin/minisat $sat_input
  python3 -s main.py --data=data --output=$output_folder_root/expression_ref/`basename $sat_input` --coding=expression_ref --solver=/usr/bin/minisat $sat_input
done
