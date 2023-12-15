#!/bin/bash
op="$1"
m="$2"
n="$3"
p="$4"
s="$5"
c="$6"
t="$7"

if ([[ "$s" -eq 1 || "$s" -eq 2 ]] && [[ "$c" -lt 0 || "$c" -gt 100 ]]); then
    echo "Error: The number of streamlining variables assigned must be between 0% and 100%"
    exit 1
fi


path_to_encoding="opb/${m}x${n}_${n}x${p}_${op}_${s}_${c}/${m}x${n}_${n}x${p}_${op}_${s}_${c}"
solver_result_file="${path_to_encoding}_solver_result.txt"
opb_path="${path_to_encoding}.opb"
drat_path="${path_to_encoding}.drat"
cnf_path="${path_to_encoding}.cnf"
drat_output="${path_to_encoding}_drat_output.txt"

echo "Running main.py..."
python3 main.py "$op" "$m" "$n" "$p" "$s" "$c"

if [ "$t" -eq 1 ]; then
    echo "Running minisat+..."
    ./minisatp/build/release/bin/minisatp $opb_path -no-pre -cnf=$cnf_path > "${path_to_encoding}_minisat_plus_output.txt"
elif [ "$t" -eq 2 ]; then
    echo "Running pblib+..."
    ./pblib/build/pbencoder $opb_path > $cnf_path
else
    echo "No translator entered! Exiting..."
    exit 2
fi


echo "Running cadical..."
./cadical/build/cadical $cnf_path $drat_path > $solver_result_file


echo "Checking if satisfiable..."
if grep -q "UNSATISFIABLE" $solver_result_file; then
    echo "The encoding is not satisfiable."
    echo "Trying to verify drat proof with drat-trim."
    ./drat-trim/drat-trim $cnf_path $drat_path > $drat_output
    if grep -q "VERIFIED" $drat_output; then
        echo "Drat proof has been verified by drat trim!"
    else
        echo "Drat proof cannot be verified!"
    fi
elif grep -q "SATISFIABLE" $solver_result_file; then
    echo "The encoding is SATISFIABLE."
    python3 verifier.py "$op" "$m" "$n" "$p" "$s" "$c"
else
    echo "The result is unknown."
fi