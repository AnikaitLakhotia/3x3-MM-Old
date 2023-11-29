import sys
from encoding import encoding
from verifier import verifier
from verifier_v2 import verifier_v2

if __name__ == '__main__':
    # Parse command line arguments
    operation = int(sys.argv[1])
    number_of_operations = int(sys.argv[2])
    m = int(sys.argv[3])
    n = int(sys.argv[4])
    p = int(sys.argv[5])
    c = sys.argv[6].lower() == 'true'
    lo = sys.argv[7].lower() == 'true'
    s0 = sys.argv[8].lower() == 'true'
    s1 = sys.argv[9].lower() == 'true'
    sp1 = int(sys.argv[10])
    s2 = sys.argv[11].lower() == 'true'
    sp2 = float(sys.argv[12])
    s3 = sys.argv[13].lower() == 'true'
    sp3 = int(sys.argv[14])
    file_path = sys.argv[15]

    # Specify parameters of the encoding
    encoding_str, cumulative_dict = encoding(number_of_operations, m, n, p, c, lo, s0, s1, sp1, s2, sp2, s3, sp3)

    if operation:
        # Write encoding to file
        with open(file_path, "w") as file:
            file.write(encoding_str)
    else:
        # If solver outputs SAT, insert the SAT assignment
        assignment_output_string = (f"logs/{number_of_operations}_{m}_{n}_{p}_{c}_{lo}"
                                    f"_{s0}_{s1}_{sp1}_{s2}_{sp2}_{s3}_{sp3}/assignment_{number_of_operations}_"
                                    f"{m}_{n}_{p}_{c}_{lo}_{s0}_{s1}_{sp1}_{s2}_{sp2}_{s3}_{sp3}.txt")
        with open(assignment_output_string, 'r') as file:
            assignment_string = file.read().rstrip('\n')

        # Removes trailing 0
        assignment_string = assignment_string[:-1]

        # Perform verifications
        verifier_output = verifier(assignment_string, cumulative_dict, number_of_operations, c)
        with open(f"logs/{number_of_operations}_{m}_{n}_{p}_{c}_{lo}"
                  f"_{s0}_{s1}_{sp1}_{s2}_{sp2}_{s3}_{sp3}/verifier_{number_of_operations}_{m}_{n}_{p}_{c}_{lo}"
                  f"_{s0}_{s1}_{sp1}_{s2}_{sp2}_{s3}_{sp3}.txt", "w") as file:
            file.write(str(verifier_output))

        verifier_v2_output = verifier_v2(assignment_string, cumulative_dict, number_of_operations, m, n, p, c)
        with open(f"logs/{number_of_operations}_{m}_{n}_{p}_{c}_{lo}"
                  f"_{s0}_{s1}_{sp1}_{s2}_{sp2}_{s3}_{sp3}/verifier_v2_{number_of_operations}_{m}_{n}_{p}_{c}_{lo}"
                  f"_{s0}_{s1}_{sp1}_{s2}_{sp2}_{s3}_{sp3}.txt", "w") as file:
            file.write(str(verifier_v2_output))
