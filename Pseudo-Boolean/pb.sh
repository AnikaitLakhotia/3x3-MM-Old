#!/bin/bash
op="$1"
m="$2"
n="$3"
p="$4"
s="$5"
c="$6"
t="$7"
e="$8"
id="$9"



check_file_existence() {
  local file_path="$1"

  if [ -e "$file_path" ]; then
    return 1
  else
    echo "File $file_path does not exist. Exiting the script."
    exit 3
  fi
}


if ([[ "$s" -eq 1 || "$s" -eq 2 ]] && [[ "$c" -lt 0 || "$c" -gt 100 ]]); then
    echo "Error: The number of streamlining variables assigned must be between 0% and 100%"
    exit 1
fi


path_to_encoding="opb/${m}x${n}_${n}x${p}_${op}_${s}_${c}_${t}_${e}_${id}/${m}x${n}_${n}x${p}_${op}_${s}_${c}_${t}_${e}_${id}"
solver_result_file="${path_to_encoding}_solver_result.txt"
opb_path="${path_to_encoding}.opb"
drat_path="${path_to_encoding}.drat"
cnf_path="${path_to_encoding}.cnf"
drat_output="${path_to_encoding}_drat_output.txt"
scheme_generated="${path_to_encoding}_scheme.txt"
verifier_matricies="${path_to_encoding}_verifier2.txt"

echo "Running main.py..."
python3 main.py "$op" "$m" "$n" "$p" "$s" "$c" "$t" "$e" "$id"
check_file_existence "$opb_path"
if [ "$t" -eq 0 ]; then
    echo "Running roundingsat"
    ./roundingsat/build/roundingsat --print-sol=1 "$opb_path" > "$solver_result_file"
    check_file_existence "$solver_result_file"
elif [ "$t" -eq 1 ]; then
    echo "Running minisat+..."
    ./minisatp/build/release/bin/minisatp "$opb_path" -no-pre -cnf="$cnf_path" > "${path_to_encoding}_minisat_plus_output.txt"
    check_file_existence "$cnf_path"
elif [ "$t" -eq 2 ]; then
    echo "Running pblib+..."
    ./pblib/build/pbencoder "$opb_path" > "$cnf_path"
    check_file_existence "$cnf_path"
else
    echo "No translator entered! Exiting..."
    exit 2
fi


if [ "$t" -eq 1 ] || [ "$t" -eq 2 ]; then
    echo "Running cadical..."
    ./cadical/build/cadical "$cnf_path" "$drat_path" > "$solver_result_file" --phase=false
    check_file_existence "$solver_result_file"
    check_file_existence "$drat_path"
fi



echo "Checking if satisfiable..."
if grep -q "UNSATISFIABLE" $solver_result_file; then
    echo "The encoding is not satisfiable."
    if [ "$t" -eq 1 ] || [ "$t" -eq 2 ]; then
        echo "Trying to verify drat proof with drat-trim."
        ./drat-trim/drat-trim $cnf_path $drat_path > $drat_output
        check_file_existence "$drat_output"
        if grep -q "VERIFIED" $drat_output; then
            echo "Drat proof has been verified by drat trim!"
        else
            echo "Drat proof cannot be verified!"
        fi
    fi
elif grep -q "SATISFIABLE" $solver_result_file; then
    echo "The encoding is SATISFIABLE."
    python3 verifier.py "$op" "$m" "$n" "$p" "$s" "$c" "$t" "$e" "$id"
    check_file_existence "$verifier_matricies"
    # python3 schemecheck.py "$scheme_generated"
else
    echo "The result is unknown."
fi
