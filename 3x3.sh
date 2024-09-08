#!/bin/bash
# Please run `chmod +x 3x3.sh` before executing the script
# to give it permission on your device

number_of_operations=$1
m=$2
n=$3
p=$4
c=$5
lo=$6
s0=$7
s1=$8
sp1=$9
s2=${10}
sp2=${11}
s3=${12}
sp3=${13}
solver=${14}
seed=${15}

var_strs=("a" "b" "g")
index=0
iter=0
prev_seed=1

#!/bin/bash

# Define the directories
initial_schemes="initial_schemes"
schemes="schemes"

# Define the directories
initial_schemes="initial_schemes"
schemes="schemes"

if [ ! -d "$schemes" ]; then
  mkdir -p "$schemes"
  echo "Created the $schemes directory."
fi

if [ "$(ls -A "$initial_schemes" 2>/dev/null)" ]; then
  mv "$initial_schemes"/* "$schemes"/
  echo "Moved all schemes from $initial_schemes to $schemes."
fi

while true; do
  var_str=${var_strs[$index]}
  seed=$((seed + 1))
  
  if [ "$test" == "1" ]; then
  directory_base="tests/logs/${number_of_operations}_${m}_${n}_${p}_${lo}_${s1}_${solver}/${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}_${iter}_${var_str}"
  else
    directory_base="logs/${number_of_operations}_${m}_${n}_${p}_${lo}_${s1}_${solver}/${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}_${iter}_${var_str}"
  fi

  directory="${directory_base}/"
  mkdir -p "$directory"

  cnf_path="${directory}instance_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}_${iter}_${var_str}.cnf"
  result="${directory}result_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}_${iter}_${var_str}.txt"

  if [ "$test" != "0" ]; then
    echo $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19}
  fi

  if [[ "${solver}" == "cadical" ]]; then
    python3 main.py 1 $number_of_operations $m $n $p $c $lo $s0 $s1 $sp1 $s2 $sp2 $s3 $sp3 $solver $seed $iter $var_str $prev_seed $cnf_path 
    ../cadical/build/cadical $cnf_path > $result --phase=false --no-binary 

    if grep -q "UNSATISFIABLE" $result; then
      cnf_path="${directory}instance_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}_${iter}_${var_str}.cnf"
      result="${directory}result_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}_${iter}_${var_str}.txt"
      python3 main.py 1 $number_of_operations $m $n $p $c $lo $s0 $s1 $sp1 $s2 $sp2 $s3 $sp3 $solver $seed $iter $var_str $prev_seed $cnf_path 

      if [ "$test" != "1" ]; then
        echo "UNSATISFIABLE"
      elif [ "$test" != "1" ] && { [ "$exp" == "0" ] || [ "$exp" == "0" ]; }; then
        echo "Test (${tc}/123) passed."
      elif [ "$test" != "1" ] && { [ "$exp" != "0" ] && [ "$exp" != "0" ]; }; then
        echo "Test (${tc}/123) failed."
      fi
      if [ "$index" -eq 2 ]; then
        iter=$((iter + 1))
        index=0
        prev_seed=1
        mv current_schemes/${number_of_operations}_${m}_${n}_${p}_${lo}_${s1}_${solver}/* schemes/${number_of_operations}_${m}_${n}_${p}_${lo}_${s1}_${solver}/
        mv current_schemes/${number_of_operations}_${m}_${n}_${p}_${lo}_${s1}_${solver}/* schemes_final/${number_of_operations}_${m}_${n}_${p}_${lo}_${s1}_${solver}/
        continue
      fi
      var_list=("a" "b" "g")

      var_str_index=-1

      for i in "${!var_list[@]}"; do
        if [[ "${var_list[$i]}" == "$var_str" ]]; then
          var_str_index=$i
          break
        fi
      done

      if [[ $var_str_index -eq -1 ]]; then
        echo "var_str not found in the list."
        exit 1
      fi

      max_seed=1
      schemes_path="schemes" 
      if [ -d "$schemes_path" ]; then
          max_seed=$(find "$schemes_path" -type f | wc -l)
          echo "The number of files in the 'schemes' directory is: $max_seed"
      else
          echo "Directory '$schemes_path' does not exist."
      fi
      
      if [ $prev_seed -eq $max_seed ]; then
        index=$(((index + 1) % 3 ))
        prev_seed=1
        continue
      fi
      prev_seed=$((prev_seed + 1))
      continue

    elif grep -q "SATISFIABLE" $result; then
      v_assignment="${directory}v_assignment_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}_${iter}_${var_str}.txt"
      assignment="${directory}assignment_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}_${iter}_${var_str}.txt"
      grep '^v ' $result  > $v_assignment
      sed 's/^v //' $v_assignment > $assignment

      if [ "$test" != "1" ]; then
        echo "SATISFIABLE"
      fi

      python3 main.py 0 $number_of_operations $m $n $p $c $lo $s0 $s1 $sp1 $s2 $sp2 $s3 $sp3 $solver $seed $iter $var_str $prev_seed $cnf_path
      verifier="${directory}verifier_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}_${iter}_${var_str}.txt"
      verifier_v2="${directory}verifier_v2_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}_${iter}_${var_str}.txt"

      if [ "$test" != "1" ]; then
        if grep -q "1" "$verifier" && grep -q "1" "$verifier_v2"; then
          message="Both verifications passed."
        elif grep -q "1" "$verifier" && grep -q "0" "$verifier_v2"; then
          message="Verification 1 passed and verification 2 failed."
        elif grep -q "0" "$verifier" && grep -q "1" "$verifier_v2"; then
          message="Verification 1 failed and verification 2 passed."
        elif grep -q "0" "$verifier" && grep -q "0" "$verifier_v2"; then
          message="Both verifications failed."
        else
          message="Error: neither SAT nor UNSAT found in cadicalResult.txt."
        fi

        echo "$message"

      elif [ "$test" == "1" ] && { [ "$exp" == "1" ] || [ "$exp" == "1" ]; }; then
        echo "Test (${tc}/123) passed."
      elif [ "$test" == "1" ] && { [ "$exp" != "1" ] && [ "$exp" != "1" ]; }; then
        echo "Test (${tc}/123) failed."
      fi
    fi

  elif [[ "${solver}" == "maplesat" ]]; then
    assignment="${directory}assignment_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
    ../maplesat/simp/maplesat_static $cnf_path $assignment > $result -phase-saving=0

    if grep -q "UNSAT" $assignment; then
      echo "UNSATISFIABLE"
    elif grep -q "SAT" $assignment; then
      echo "SATISFIABLE"
      python3 main.py 0 $number_of_operations $m $n $p $c $lo $s0 $s1 $sp1 $s2 $sp2 $s3 $sp3 $solver $seed $cnf_path
      verifier="${directory}verifier_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
      verifier_v2="${directory}verifier_v2_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
      if grep -q "1" $verifier; then
        echo "The scheme has been verified by the first verifier."
      else
        echo "The scheme cannot be verified."
      fi
      if grep -q "1" $verifier_v2; then
        echo "The scheme has been verified by the second verifier."
      else
        echo "The scheme cannot be verified by the second verifier."
      fi
    fi

  elif [[ "${solver}" == "yalsat" ]]; then
    ../yalsat/yalsat $cnf_path > $result

    if grep -q "UNSATISFIABLE" $result; then
      echo "UNSATISFIABLE"
    elif grep -q "SATISFIABLE" $result; then
      v_assignment="${directory}v_assignment_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
      assignment="${directory}assignment_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
      grep '^v ' $result  > $v_assignment
      sed 's/^v //' $v_assignment > $assignment
      echo "SATISFIABLE"
      python3 main.py 0 $number_of_operations $m $n $p $c $lo $s0 $s1 $sp1 $s2 $sp2 $s3 $sp3 $solver $seed $cnf_path
      verifier="${directory}verifier_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
      verifier_v2="${directory}verifier_v2_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
      if grep -q "1" $verifier; then
        echo "The scheme has been verified by the first verifier."
      else
        echo "The scheme cannot be verified."
      fi
      if grep -q "1" $verifier_v2; then
        echo "The scheme has been verified by the second verifier."
      else
        echo "The scheme cannot be verified by the second verifier."
      fi
    else
      echo "Error: neither SAT nor UNSAT found in result file."
    fi
  fi
done
