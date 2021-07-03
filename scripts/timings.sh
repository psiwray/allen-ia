#!/bin/bash

if [[ $# -lt 2 ]]; then
  echo "Missing required arguments."
  exit -1
fi

iterations=$1
timer_file=$2

rm -rf $timer_file 2>/dev/null
echo "generator_ternary_impl,generator_expression_ref,solver_ternary_impl,solver_expression_ref" > $timer_file

for i in `seq 1 $iterations`; do
  echo "Working with iteration $i."

  output=`bash test.sh 1`
  if [[ $? -ne 0 ]]; then
    echo "Failed to process this iteration."
    exit -1
  fi

  # Find the total clauses and literals that have been generated for both inputs.
  total_clauses=`echo $output | grep -oE "A total of [0-9]+ clauses have been generated." | grep -oE "[0-9]+"`
  total_clauses_ternary_impl=`echo $total_clauses | cut -f 1 -d " "`
  total_clauses_expression_ref=`echo $total_clauses | cut -f 2 -d " "`
  total_literals=`echo $output | grep -oE "A total of [0-9]+ literals have been used." | grep -oE "[0-9]+"`
  total_literals_ternary_impl=`echo $total_literals | cut -f 1 -d " "`
  total_literals_expression_ref=`echo $total_literals | cut -f 2 -d " "`

  # Find the time it took to generate the boolean expression.
  generation_time=`echo $output | grep -oE "[0-9]+.[0-9]+s"`
  generation_time_ternary_impl=`echo $generation_time | cut -f 1 -d " " | tr -d "s" | tr -d "[:space:]"`
  generation_time_expression_ref=`echo $generation_time | cut -f 2 -d " " | tr -d "s" | tr -d "[:space:]"`

  # Now go find the CPU time for both results and put it into a common CSV file.
  timing_ternary_impl=`cat output/ternary_impl/test/intervals.txt/timings.txt | cut -d ":" -f 2 | cut -d "s" -f 1 | tr -d "[:space:]"`
  timing_expression_ref=`cat output/expression_ref/test/intervals.txt/timings.txt | cut -d ":" -f 2 | cut -d "s" -f 1 | tr -d "[:space:]"`
  echo "$total_clauses_ternary_impl,$total_clauses_expression_ref,$total_literals_ternary_impl,$total_literals_expression_ref,$generation_time_ternary_impl,$generation_time_expression_ref,$timing_ternary_impl,$timing_expression_ref" >> $timer_file
done

echo "Completed $iterations iterations."
