#!/bin/bash
# Please run `chmod +x 3x3.sh` before executing the script 
# to give it permission on your device

# stucture your directory as follows:
  # ---- 3x3-MM
  # ---- cadical
  # ---- drat-trime


# path to .cnf file
cnf_path="instance.cnf"
# path to .drat file
drat_path="instance.drat"
# number of operations for multiplication
number_of_operations=9
# number of rows in matrix B
m=2
# number of cols in matrix A and rows in matrix B
n=2
# number of cols in matrix B
p=2
python3 main.py 1 $number_of_operations $m $n $p $cnf_path
../cadical/build/cadical $cnf_path $drat_path > cadicalResult.txt

# Check if "UNSATISFIABLE" is in cadicalResult.txt
if grep -q "UNSATISFIABLE" cadicalResult.txt; then
    # If "UNSATISFIABLE" is found, run ./drat-trim
    echo "UNSATISFIABLE"
    ../drat-trim/drat-trim $cnf_path $drat_path > drat_output.txt
    if grep -q "VERIFIED" drat_output.txt; then
      echo "UNSAT proof is verified by DRAT"
    else
      echo "UNSAT proof cannot not verified by DRAT"
    fi
else
    # If "UNSATISFIABLE" (meaning the result is SAT) is not found, run python3 verifier.py
    grep '^v ' cadicalResult.txt  > v_assignment.txt
    sed 's/^v //' v_assignment.txt > assignment.txt
    echo "SATISFIABLE"
    python3 main.py 0 $number_of_operations $m $n $p $cnf_path
    if grep -q "1" verifier.txt; then
      echo "The scheme has been verified."
    else
      echo "The scheme cannot be verified."
    fi
fi