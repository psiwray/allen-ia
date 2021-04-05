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

  echo "Finished generating boolean expressions, now checking."
  for sat in $folder/$generation/ternary_impl/*.sat; do
    minisat $sat >> $folder/$generation/ternary_impl/log.txt
  done
  for sat in $folder/$generation/expression_ref/*.sat; do
    minisat $sat >> $folder/$generation/expression_ref/log.txt
  done

  grep "UNSATISFIABLE" $folder/$generation/ternary_impl/log.txt
  grep "UNSATISFIABLE" $folder/$generation/expression_ref/log.txt
done
