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
directory="logs/${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}/"

if [ "$test" == "1" ]; then
  directory="tests/logs/${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}/"
else
  directory="logs/${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}/"
fi

mkdir -p "$directory"

cnf_path="${directory}instance_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.cnf"
result="${directory}result_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"

if [ "$test" != "0" ]; then
  echo $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14} ${15}
fi

python3 main.py 1 $number_of_operations $m $n $p $c $lo $s0 $s1 $sp1 $s2 $sp2 $s3 $sp3 $solver $seed $cnf_path

if [[ "${solver}" == "cadical" ]]; then :
  ../cadical/build/cadical $cnf_path > $result --phase=false --no-binary

  # Check if "UNSATISFIABLE" is in cadicalResult.txt
  if grep -q "UNSATISFIABLE" $result; then :
      # If "UNSATISFIABLE" is found, run ./drat-trim

      if [ "$test" != "1" ]; then
        echo "UNSATISFIABLE"
      elif [ "$test" != "1" ] && { [ "$exp" == "0" ] || [ "$exp" == "0" ]; }; then
        echo "Test (${tc}/123) passed."
      elif [ "$test" != "1" ] && { [ "$exp" != "0" ] && [ "$exp" != "0" ]; }; then
        echo "Test (${tc}/123) failed."
      fi

  elif grep -q "SATISFIABLE" $result; then :
      # If "SATISFIABLE" is found, run python3 verifier.py
      v_assignment="${directory}v_assignment_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
      assignment="${directory}assignment_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
      grep '^v ' $result  > $v_assignment
      sed 's/^v //' $v_assignment > $assignment

      if [ "$test" != "1" ]; then
        echo "SATISFIABLE"
      fi

      python3 main.py 0 $number_of_operations $m $n $p $c $lo $s0 $s1 $sp1 $s2 $sp2 $s3 $sp3 $solver $seed $cnf_path
      verifier="${directory}verifier_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
      verifier_v2="${directory}verifier_v2_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"

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
elif [[ "${solver}" == "maplesat" ]]; then :
  assignment="${directory}assignment_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
  ../maplesat/simp/maplesat_static $cnf_path $assignment > $result -phase-saving=0

  if grep -q "UNSAT" $assignment; then :
    echo "UNSATISFIABLE"
  elif grep -q "SAT" $assignment; then :
    echo "SATISFIABLE"
    python3 main.py 0 $number_of_operations $m $n $p $c $lo $s0 $s1 $sp1 $s2 $sp2 $s3 $sp3 $solver $seed $cnf_path
    verifier="${directory}verifier_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
    verifier_v2="${directory}verifier_v2_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
      if grep -q "1" $verifier; then :
        echo "The scheme has been verified by the first verifier."
      else
        echo "The scheme cannot be verified."
      fi
      if grep -q "1" $verifier_v2; then :
          echo "The scheme has been verified by the second verifier."
        else
          echo "The scheme cannot be verified by the second verifier."
      fi
  fi
elif [[ "${solver}" == "yalsat" ]]; then :
  ../yalsat/yalsat $cnf_path > $result

  if grep -q "UNSATISFIABLE" $result; then :
      echo "UNSATISFIABLE"
  elif grep -q "SATISFIABLE" $result; then :
      # If "SATISFIABLE" is found, run python3 verifier.py
      v_assignment="${directory}v_assignment_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
      assignment="${directory}assignment_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
      grep '^v ' $result  > $v_assignment
      sed 's/^v //' $v_assignment > $assignment
      echo "SATISFIABLE"
      python3 main.py 0 $number_of_operations $m $n $p $c $lo $s0 $s1 $sp1 $s2 $sp2 $s3 $sp3 $solver $seed $cnf_path
      verifier="${directory}verifier_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
      verifier_v2="${directory}verifier_v2_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
      if grep -q "1" $verifier; then :
        echo "The scheme has been verified by the first verifier."
      else
        echo "The scheme cannot be verified."
      fi
      if grep -q "1" $verifier_v2; then :
          echo "The scheme has been verified by the second verifier."
        else
          echo "The scheme cannot be verified by the second verifier."
      fi
      else :
      echo "Error: neither SAT nor UNSAT found in cadicalResult.txt."
  fi
fi
