#!/bin/bash

instance=$1
total_groups=$2
output_folder=output/all
log=$output_folder/mismatching_groups.txt

rm -rf output/all
rm -rf $log

for group in `seq 0 $(( $total_groups - 1 ))`; do
  python3 -s main.py \
      --output=$output_folder/ternary_impl \
      --coding=ternary_impl \
      --data=data \
      --solver=/usr/bin/minisat \
      --groups=$group \
      $instance
  python3 -s main.py \
      --output=$output_folder/expression_ref \
      --coding=expression_ref \
      --data=data \
      --solver=/usr/bin/minisat \
      --groups=$group \
      $instance

  result_ternary_impl=`grep "SATISFIABLE\|UNSATISFIABLE" $output_folder/ternary_impl/$group/solver_log.txt`
  result_expression_ref=`grep "SATISFIABLE\|UNSATISFIABLE" $output_folder/expression_ref/$group/solver_log.txt`

  if [[ $result_ternary_impl != $result_expression_ref ]]; then
    echo "Group $group has different results: $result_ternary_impl, $result_expression_ref."
    echo $group >> $log
  fi
done
