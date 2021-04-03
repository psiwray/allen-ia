#!/bin/bash

function call_script {
  coding=$1
  output_dir=$2
  time_intervals_file=$3
  python3 -s main.py --data=data --coding=$coding --output=$output_dir $time_intervals_file
}

output=$1
output_ternary_impl="$output-ternary_impl.csv"
output_expression_ref="$output-expression_ref.csv"
echo "nome_istanza,gruppo_istanza,risultato,numero_variabili,numero_clausole,riavvii,conflitti,decisioni,propagazioni,conflitto_letterali,tempo_cpu" > $output_ternary_impl
echo "nome_istanza,gruppo_istanza,risultato,numero_variabili,numero_clausole,riavvii,conflitti,decisioni,propagazioni,conflitto_letterali,tempo_cpu" > $output_expression_ref

for time_intervals_file in data/time_intervals/*.txt; do
  echo "Executing time intervals file $time_intervals_file."
  for coding in ternary_impl expression_ref; do
    # Compute the SAT boolean expression for every group contained in the file.
    output_folder=output/$coding/`basename $time_intervals_file`
    call_script $coding $output_folder $time_intervals_file
    # Then call the SAT solver on it and record the results on the file.
    for sat_file in $output_folder/*.sat; do
      log_file=".log.txt"
      minisat $sat_file &> $log_file

      # Check results and write them.
      group_name=`basename $time_intervals_file | cut -f 1 -d '.'`
      group_id=`basename $sat_file | cut -f 1 -d '.'`
      satisfiability=`cat $log_file | grep -e "UNSATISFIABLE\|SATISFIABLE"`
      variable_count=`cat $log_file | grep "Number of variables:" | grep -oE "[[:blank:]][[:digit:]]+[[:blank:]]"`
      clause_count=`cat $log_file | grep "Number of clauses:" | grep -oE "[[:blank:]][[:digit:]]+[[:blank:]]"`
      restarts=`cat $log_file | grep "restarts" | grep -oE "[[:blank:]][[:digit:]]+"`
      conflicts=`cat $log_file | grep "conflicts" | grep -oE "[[:blank:]][[:digit:]]+[[:blank:]]"`
      decisions=`cat $log_file | grep "decisions" | grep -oE "[[:blank:]][[:digit:]]+[[:blank:]]"`
      propagations=`cat $log_file | grep "propagations" | grep -oE "[[:blank:]][[:digit:]]+[[:blank:]]"`
      conflict_literals=`cat $log_file | grep "conflict literals" | grep -oE "[[:blank:]][[:digit:]]+[[:blank:]]"`
      cpu_time=`cat $log_file | grep "CPU time" | grep -oE "[[:digit:]]+.[[:digit:]]+[[:blank:]]"`

      echo -n "$group_name,$group_id,$satisfiability,$variable_count,$clause_count,$restarts,$conflicts,$decisions,$propagations,$conflict_literals,$cpu_time" | tr -d ' ' >> "$output-$coding.csv"
      echo "" >> "$output-$coding.csv"
      rm -rf $log_file
    done
  done
done
