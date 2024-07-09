#!/bin/bash

# Ensure we are in the root directory of the repo
ROOT_DIR=$(git rev-parse --show-toplevel)
cd "$ROOT_DIR"

# Define the target directory
TARGET_DIR="$ROOT_DIR/Pseudo-Boolean"

# Clone each repository into the target directory
echo "Cloning cadical..."
git clone https://github.com/arminbiere/cadical.git "$TARGET_DIR/cadical"

echo "Cloning pblib..."
git clone https://github.com/aayushkapoor1/pblib.git "$TARGET_DIR/pblib"

echo "Cloning drat-trim..."
git clone https://github.com/marijnheule/drat-trim.git "$TARGET_DIR/drat-trim"

# Build cadical
echo "Building cadical..."
cd "$TARGET_DIR/cadical"
mkdir build
cd build
for f in ../src/*.cpp; do g++ -O3 -DNDEBUG -DNBUILD -c $f; done
ar rc libcadical.a `ls *.o | grep -v ical.o`
g++ -o cadical cadical.o -L. -lcadical
g++ -o mobical mobical.o -L. -lcadical

echo "cadical build completed."

# Build drat-trim
echo "Building drat-trim..."
cd "$TARGET_DIR/drat-trim"
make         # Build drat-trim

echo "drat-trim build completed."
