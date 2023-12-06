#!/bin/bash
op="$1"
m="$2"
n="$3"
p="$4"
s="$5"
c="$6"

if ([[ "$s" -eq 1 || "$s" -eq 2 ]] && [[ "$c" -lt 0 || "$c" -gt 100 ]]); then
    echo "Error: The number of streamlining variables assigned must be between 0% and 100%"
    exit 1
fi


path_to_encoding="opb/${m}x${n}_${n}x${p}_${op}_${s}_${c}/${m}x${n}_${n}x${p}_${op}_${s}_${c}"

echo "Running main.py..."
python3 main.py "$op" "$m" "$n" "$p" "$s" "$c"

echo "Running minisat+..."
./minisatp/build/release/bin/minisatp "${path_to_encoding}.opb" -cnf="${path_to_encoding}.cnf" > "${path_to_encoding}_minisat_plus_output.txt"

echo "Running cadical..."
./cadical/build/cadical "${path_to_encoding}.cnf" > "${path_to_encoding}_solver_result.txt"

exit 1

# echo "Running roundingsat..."

# ./roundingsat/build/roundingsat "${path_to_encoding}.opb" --print-sol=1 > "${path_to_encoding}_assignment.txt"

echo "Checking if satisfiable..."
if grep -q "UNSATISFIABLE" "${path_to_encoding}_assignment.txt"; then
    echo "The encoding is not satisfiable."
elif grep -q "SATISFIABLE" "${path_to_encoding}_assignment.txt"; then
    echo "The encoding is SATISFIABLE."
    python3 verifier.py "$op" "$m" "$n" "$p" "$s" "$c"
else
    echo "The result is unknown."
fi