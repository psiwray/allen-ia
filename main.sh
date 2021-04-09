#!/bin/bash

if [[ $# -eq 0 ]]; then
  echo "Missing time intervals."
  exit -1
fi

while [[ $# -gt 0 ]]; do
  time_intervals_file=$1
  shift

  coding="ternary_impl"
  python3 -s main.py \
      --data=data \
      --output=output/$coding/$time_intervals_file \
      --coding=$coding \
      --solver=/usr/bin/minisat \
      data/time_intervals/$time_intervals_file
  coding="expression_ref"
  python3 -s main.py \
      --data=data \
      --output=output/$coding/$time_intervals_file \
      --coding=$coding \
      --solver=/usr/bin/minisat \
      data/time_intervals/$time_intervals_file

  rm output/ternary_impl/$time_intervals_file/timings.txt 2>/dev/null
  rm output/expression_ref/$time_intervals_file/timings.txt 2>/dev/null
  for log in `find output/ternary_impl -name solver_log.txt`; do
    grep "CPU time" $log >> output/ternary_impl/$time_intervals_file/timings.txt
  done
  for log in `find output/expression_ref -name solver_log.txt`; do
    grep "CPU time" $log >> output/expression_ref/$time_intervals_file/timings.txt
  done
done
