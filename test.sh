#!/bin/bash

groups=$1
size=$2
iterations=$3

gqr_dir=$HOME/Repositories/gqr
instance_file=output/instance.txt

for _ in `seq 1 $iterations`; do
  rm -rf output/*

  # First generate a valid instance.
  perl $gqr_dir/tools/gencsp.pl \
      --size=$size \
      --data-dir=$gqr_dir/data \
      --calculus=allen \
      --number=$groups \
      --degree=3 > $instance_file

  # Now execute the program on this newly generated instance.
  python3 -s main.py \
      --output=output/ternary_impl \
      --data=data \
      --coding=ternary_impl \
      --solver=/usr/bin/minisat $instance_file
  python3 -s main.py \
      --output=output/expression_ref \
      --data=data \
      --coding=expression_ref \
      --solver=/usr/bin/minisat $instance_file

  found=0
  for log in `find output/ -name solver_log.txt`; do
    if [[ `grep "UNSATISFIABLE" $log | wc -l` -gt 0 ]]; then
      echo "Found unsatisfiable instance group in $log."
      found=1
    fi
  done

  if [[ $found -eq 1 ]]; then
    exit -1
  fi
done
