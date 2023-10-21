import sys
import os
from encoding import encoding
from verifier import verifier
from verifier_v2 import verifier_v2
if __name__ == '__main__':
    operation = int(sys.argv[1])
    number_of_operations = int(sys.argv[2])
    m = int(sys.argv[3])
    n = int(sys.argv[4])
    p = int(sys.argv[5])
    file_path = sys.argv[6]

    # Specify parameters of the encoding
    encoding, cumulative_dict = encoding(number_of_operations, m, n, p, 3)
    if operation:
        # Open file and write data to it
        with open(file_path, "w") as file:
            file.write(encoding)
    else:
        # If solver outputs SAT, insert the SAT assignment
        assignment_output_string = f"logs/{number_of_operations}_{m}_{n}_{p}/assignment_{number_of_operations}_{m}_{n}_{p}.txt"
        with open(assignment_output_string, 'r') as file:
            assignment_string = file.read().rstrip('\n')

        # removes trailing 0
        assignment_string = assignment_string[:-1]

        verifier_output = verifier(assignment_string, cumulative_dict, number_of_operations)
        with open(f"logs/{number_of_operations}_{m}_{n}_{p}/verifier_{number_of_operations}_{m}_{n}_{p}.txt", "w") as file:
            file.write(str(verifier_output))

        verifier_v2_output = verifier_v2(assignment_string, cumulative_dict, number_of_operations, m, n, p)
        with open(f"logs/{number_of_operations}_{m}_{n}_{p}/verifier_v2_{number_of_operations}_{m}_{n}_{p}.txt", "w") as file:
            file.write(str(verifier_v2_output))
