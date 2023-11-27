#!/bin/bash

function run_experiment {
    local op=$1
    local m=$2
    local n=$3
    local p=$4
    local s=$5
    local c=$6

    timeout 10m make op=$op m=$m n=$n p=$p s=$s c=$c
    result=$?

    if [ $result -eq 124 ]; then
        echo "Command timed out after 10 minutes."
    elif [ $result -eq 0 ]; then
        echo "Command completed successfully."
    else
        echo "Command failed with exit code $result."
    fi
}

function miscellaneous_matrix_sizes {
    run_experiment 9 3 1 3 0 0
    run_experiment 10 2 1 5 0 0
    run_experiment 11 1 1 11 0 0
    run_experiment 2 2 1 1 0 0
    run_experiment 3 1 3 1 0 0
    run_experiment 4 2 2 1 0 0
    run_experiment 5 1 5 1 0 0
    run_experiment 6 2 3 1 0 0
}

function 3x3_23_multiplications {
    run_experiment 23 3 3 3 1 1
    run_experiment 23 3 3 3 1 0.9
    run_experiment 23 3 3 3 1 0.8
    run_experiment 23 3 3 3 1 0.7
    run_experiment 23 3 3 3 1 0.6
    run_experiment 23 3 3 3 1 0.5
}
