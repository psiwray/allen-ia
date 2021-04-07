#!/bin/bash

intervals=$1
time=$2
iterations=$3
groups=$4
generations=$5
folder=$6

rm -rf $folder
mkdir -p $folder

for generation in `seq 1 $generations`; do
  mkdir $folder/$generation

  echo "Generating new random instance number $generation."
  python3 -s generator.py --total-intervals=$intervals --max-time=$time --iterations=$iterations --groups=$groups > $folder/$generation/instance.sat
  python3 -s main.py --data=data --output=$folder/$generation/ternary_impl --coding=ternary_impl $folder/$generation/instance.sat
  python3 -s main.py --data=data --output=$folder/$generation/expression_ref --coding=expression_ref $folder/$generation/instance.sat

  for file in `find generation/ -name solver_log.txt`; do
    grep "UNSATISFIABLE" $file
  done
done
