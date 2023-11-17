op="$1"
m="$2"
n="$3"
p="$4"

path_to_encoding="opb/${m}x${n}_${n}x${p}_${op}/${m}x${n}_${n}x${p}_${op}"

echo "Running main.py..."
python3 main.py "$op" "$m" "$n" "$p"

echo "Running roundingsat..."
../../roundingsat/build/roundingsat "${path_to_encoding}.opb" --print-sol=1 >> "${path_to_encoding}_assignment.txt"

echo "Checking if satisfiable..."
if grep -q "UNSATISFIABLE" "${path_to_encoding}_assignment.txt"; then
    echo "The solution is not satisfiable."
else
    echo "The solution is SATISFIABLE."
    python3 verifier.py "$op" "$m" "$n" "$p"
fi