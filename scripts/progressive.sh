iterations=$1
min_degree=`echo $2 | cut -f 1 -d ":"`
max_degree=`echo $2 | cut -f 2 -d ":"`
min_size=`echo $3 | cut -f 1 -d ":"`
max_size=`echo $3 | cut -f 2 -d ":"`
data_folder=$4
output_folder=$5
output_file=$6

total_degree_excursion=$(($max_degree - $min_degree))
total_size_excursion=$(($max_size - $min_size))
degree_step=`echo "scale=5; $total_degree_excursion / $iterations" | bc`
size_step=`echo "scale=5; $total_size_excursion / $iterations" | bc`

rm -rf $output_folder
rm -rf $output_file
mkdir -p $data_folder
mkdir -p $output_folder/{ternary_impl,expression_ref}
echo "i,degree,size,literals_ibsc,clauses_ibsc,literals_gac,clauses_gac,solve_time_ibsc,solve_time_gac,sat_ibsc,sat_gac" > $output_file

for i in `seq 1 $iterations`; do
  echo "Iteration $i."
  current_degree=`echo "scale=5; $min_degree + $i * $degree_step" | bc | cut -f 1 -d "."`
  current_size=`echo "scale=5; $min_size + $i * $size_step" | bc | cut -f 1 -d "."`

  # Generate the time intervals.
  perl /home/psiwray/Repositories/gqr/tools/gencsp.pl \
    --calculus=allen \
    --degree=$current_degree \
    --number=1 \
    --size=$current_size \
    --data-dir=/home/psiwray/Repositories/gqr/data > $data_folder/$i.txt

  # Run the generation script.
  python3 -s main.py \
      --data=data \
      --output=$output_folder/ternary_impl/$i \
      --coding="ternary_impl" \
      --solver=/usr/bin/minisat \
      $data_folder/$i.txt

  python3 -s main.py \
      --data=data \
      --output=$output_folder/expression_ref/$i \
      --coding="expression_ref" \
      --solver=/usr/bin/minisat \
      $data_folder/$i.txt

  # Now collect timing information.
  solver_log_ibsc=$output_folder/ternary_impl/$i/0/solver_log.txt
  solver_log_gac=$output_folder/expression_ref/$i/0/solver_log.txt

  variables_ibsc=`grep -oE "Number of variables:[[:space:]]+[[:digit:]]+" $solver_log_ibsc | cut -f 2 -d ":" | tr -d "[:space:]"`
  variables_gac=`grep -oE "Number of variables:[[:space:]]+[[:digit:]]+" $solver_log_gac | cut -f 2 -d ":" | tr -d "[:space:]"`
  clauses_ibsc=`grep -oE "Number of clauses:[[:space:]]+[[:digit:]]+" $solver_log_ibsc | cut -f 2 -d ":" | tr -d "[:space:]"`
  clauses_gac=`grep -oE "Number of clauses:[[:space:]]+[[:digit:]]+" $solver_log_gac | cut -f 2 -d ":" | tr -d "[:space:]"`
  cpu_time_ibsc=`grep "CPU time" $solver_log_ibsc | grep -oE "[[:digit:]]+(.[[:digit:]]+)?"`
  cpu_time_gac=`grep "CPU time" $solver_log_gac | grep -oE "[[:digit:]]+(.[[:digit:]]+)?"`
  sat_ibsc=`grep "SATISFIABLE\|UNSATISFIABLE" $solver_log_ibsc`
  sat_gac=`grep "SATISFIABLE\|UNSATISFIABLE" $solver_log_gac`

  echo "$i,$current_degree,$current_size,$variables_ibsc,$variables_gac,$clauses_ibsc,$clauses_gac,$cpu_time_ibsc,$cpu_time_gac,$sat_ibsc,$sat_gac" >> $output_file

  # Remove the output to keep the disk free.
  rm -rf $output_folder/ternary_impl/$i
  rm -rf $output_folder/expression_ref/$i
done
