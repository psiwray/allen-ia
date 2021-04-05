#!/bin/bash

input_time_intervals=$1
output_folder_root=$2
csv_dump=$3

for sat_input in $input_time_intervals/*.txt; do
  echo "Executing instance $sat_input."
  python3 -s main.py --data=data --output=$output_folder_root/ternary_impl/`basename $sat_input` --coding=ternary_impl --solver=/usr/bin/minisat $sat_input
  python3 -s main.py --data=data --output=$output_folder_root/expression_ref/`basename $sat_input` --coding=expression_ref --solver=/usr/bin/minisat $sat_input
done

echo "istanza,gruppo,risultato,variabili,clausole,riavvii,conflitti,decisioni,propagazioni,conflitto_letterali,tempo_cpu" > ${csv_dump}_ternary_impl.csv
echo "istanza,gruppo,risultato,variabili,clausole,riavvii,conflitti,decisioni,propagazioni,conflitto_letterali,tempo_cpu" > ${csv_dump}_expression_ref.csv

# Gather all results inside a CSV-formatted file.
for coding in ternary_impl expression_ref; do
  for instance_name in $output_folder_root/$coding/*.txt; do
    for group_number in $instance_name/*; do
      group_number=`basename $group_number`
      results_file="$instance_name/$group_number/solver_log.txt"

      satisfiable=`cat $results_file | grep -o "UNSATISFIABLE\|SATISFIABLE"`
      variables=`cat $results_file | grep "Number of variables:" | grep -oE "[[:digit:]]+"`
      clauses=`cat $results_file | grep "Number of clauses:" | grep -oE "[[:digit:]]+"`
      restarts=`cat $results_file | grep "restarts" | grep -oE "[[:blank:]]+[[:digit:]]+"`
      conflicts=`cat $results_file | grep "conflicts" | grep -oE "[[:blank:]]+[[:digit:]]+[[:blank:]]"`
      decisions=`cat $results_file | grep "decisions" | grep -oE "[[:blank:]]+[[:digit:]]+[[:blank:]]"`
      propagations=`cat $results_file | grep "propagations" | grep -oE "[[:blank:]]+[[:digit:]]+[[:blank:]]"`
      conflict_literals=`cat $results_file | grep "conflict literals" | grep -oE "[[:blank:]]+[[:digit:]]+[[:blank:]]"`
      cpu_time=`cat $results_file | grep "CPU time" | grep -oE "[[:digit:]]+(.[[:digit:]]+)? s"`

      instance=`basename $instance_name | cut -d "." -f 1`
      group=$group_number

      echo "$instance,$group,$satisfiable,$variables,$clauses,$restarts,$conflicts,$decisions,$propagations,$conflict_literals,$cpu_time" >> ${csv_dump}_$coding.csv
    done
  done
done
