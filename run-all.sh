#!/bin/bash

methods="ternary_impl expression_ref"
time_intervals=`ls data/time_intervals/*.txt`

for method in $methods; do
  echo "Using method: $method."
  for time_interval in $time_intervals; do
    echo "Working with time interval $time_interval."
    bash run.sh $time_interval $method
  done

  # Also run tests.
  bash run.sh data/time_intervals/test/3.txt $method
  bash run.sh data/time_intervals/test/4.txt $method
done


