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

mkdir -p "$directory"

cnf_path="${directory}instance_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.cnf"
result="${directory}result_${number_of_operations}_${m}_${n}_${p}_${c}_${lo}_${s0}_${s1}_${sp1}_${s2}_${sp2}_${s3}_${sp3}_${solver}_${seed}.txt"
echo $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14} ${15}
python3 main.py 1 $number_of_operations $m $n $p $c $lo $s0 $s1 $sp1 $s2 $sp2 $s3 $sp3 $solver $seed $cnf_path

if [[ "${14}" == "cadical" ]]; then :
  ../cadical/build/cadical $cnf_path > $result --phase=false

  # Check if "UNSATISFIABLE" is in cadicalResult.txt
  if grep -q "UNSATISFIABLE" $result; then :
      # If "UNSATISFIABLE" is found, run ./drat-trim
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
        echo "The scheme has been verified by first verifier."
      else
        echo "The scheme cannot be verified."
      fi
      if grep -q "1" $verifier_v2; then :
          echo "The scheme has been verified by second verifier."
        else
          echo "The scheme cannot be verified by second verifier."
      fi
      else :
      echo "Error: neither SAT nor UNSAT found in cadicalResult.txt."
  fi
elif [[ "${14}" == "maplesat" ]]; then :
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
        echo "The scheme has been verified by first verifier."
      else
        echo "The scheme cannot be verified."
      fi
      if grep -q "1" $verifier_v2; then :
          echo "The scheme has been verified by second verifier."
        else
          echo "The scheme cannot be verified by second verifier."
      fi
  fi
elif [[ "${14}" == "yalsat" ]]; then :
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
        echo "The scheme has been verified by first verifier."
      else
        echo "The scheme cannot be verified."
      fi
      if grep -q "1" $verifier_v2; then :
          echo "The scheme has been verified by second verifier."
        else
          echo "The scheme cannot be verified by second verifier."
      fi
      else :
      echo "Error: neither SAT nor UNSAT found in cadicalResult.txt."
  fi
fi
