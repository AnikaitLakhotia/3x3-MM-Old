#!/bin/bash
# Please run `chmod +x 3x3.sh` before executing the script 
# to give it permission on your device

# stucture your directory as follows:
  # ---- 3x3-MM
  # ---- cadical
  # ---- drat-trime


if [ "$#" -ne 4 ]; then
  echo "Four variables are required"
  exit 1
fi

number_of_operations=$1
m=$2
n=$3
p=$4
directory="logs/${number_of_operations}_${m}_${n}_${p}/"

mkdir -p "$directory"

cnf_path="${directory}instance_${number_of_operations}_${m}_${n}_${p}.cnf"
drat_path="${directory}instance_${number_of_operations}_${m}_${n}_${p}.drat"
cadical_result="${directory}cadical_result_${number_of_operations}_${m}_${n}_${p}.txt"
echo $1 $2 $3 $4
python3 main.py 1 $number_of_operations $m $n $p $cnf_path
../cadical/build/cadical $cnf_path $drat_path > $cadical_result

# Check if "UNSATISFIABLE" is in cadicalResult.txt
if grep -q "UNSATISFIABLE" $cadical_result; then
    # If "UNSATISFIABLE" is found, run ./drat-trim
    echo "UNSATISFIABLE"
    drat_output="${directory}drat_output_${number_of_operations}_${m}_${n}_${p}.txt"
    ./drat-trim/drat-trim $cnf_path $drat_path > $drat_output
    if grep -q "VERIFIED" $drat_output; then
      echo "UNSAT proof is verified by DRAT"
    else
      echo "UNSAT proof cannot not verified by DRAT"
    fi
else
    # If "UNSATISFIABLE" is not found(meaning the result is SAT), run python3 verifier.py
    v_assignment="${directory}v_assignment_${number_of_operations}_${m}_${n}_${p}.txt"
    assignment="${directory}assignment_${number_of_operations}_${m}_${n}_${p}.txt"
    grep '^v ' $cadical_result  > $v_assignment
    sed 's/^v //' $v_assignment > $assignment
    echo "SATISFIABLE"
    python3 main.py 0 $number_of_operations $m $n $p $cnf_path
    verifier="${directory}verifier_${number_of_operations}_${m}_${n}_${p}.txt"
    verifier_v2="${directory}verifier_v2_${number_of_operations}_${m}_${n}_${p}.txt"
    if grep -q "1" $verifier; then
      echo "The scheme has been verified by first verifier."
    else
      echo "The scheme cannot be verified."
    fi
    if grep -q "1" $verifier_v2; then
        echo "The scheme has been verified by second verifier."
      else
        echo "The scheme cannot be verified by second verifier."
    fi
fi