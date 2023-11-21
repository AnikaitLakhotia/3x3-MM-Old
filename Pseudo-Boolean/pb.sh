op="$1"
m="$2"
n="$3"
p="$4"
s="$5"

path_to_encoding="opb/${m}x${n}_${n}x${p}_${op}_${s}/${m}x${n}_${n}x${p}_${op}_${s}"

echo "Running main.py..."
python3 main.py "$op" "$m" "$n" "$p" "$s"

echo "Running roundingsat..."
../../roundingsat/build/roundingsat "${path_to_encoding}.opb" --print-sol=1 --proof-log="${path_to_encoding}" > "${path_to_encoding}_assignment.txt"

echo "Checking if satisfiable..."
if grep -q "UNSATISFIABLE" "${path_to_encoding}_assignment.txt"; then
    echo "The solution is not satisfiable."
else
    echo "The solution is SATISFIABLE."
    python3 verifier.py "$op" "$m" "$n" "$p" "$s"
fi