import sys
from encoding import encoding
from verifier import verifier
from verifier_v2 import verifier_v2
from scheme import scheme
import os

if __name__ == '__main__':
    try:
        # Input validation and value checks
        if len(sys.argv) != 21:
            raise ValueError("Incorrect number of arguments. Usage: make op= m= "
                             "n= p= c= lo= s0= s1= sp1= s2= sp2= s3= sp3= solver= seed=")

        # Indices of command line arguments that should be integers
        int_arg_indices = [1, 2, 3, 4, 5, 10, 14, 17]

        # Indices of command line arguments that should be bools
        bool_arg_indices = [6, 7, 8, 9, 11, 13]

        for index in int_arg_indices:
            try:
                # Try to convert the argument to an integer
                int(sys.argv[index])

            except ValueError:
                # Raise an exception if the conversion fails
                raise TypeError(f'Error: Argument at index {index} should be an integer.')

        for index in bool_arg_indices:
            if sys.argv[index] != "True" and sys.argv[index] != "False":
                # Raise an exception if the argument is neither "True" nor "False
                raise TypeError(f'Error: Argument at index {index} should be True or False.')

        try:
            # Try to convert argument 12 to a float
            float(sys.argv[12])

        except ValueError:
            # Raise an exception if the conversion fails
            raise TypeError(f'Error: Argument at index 12 should be a float.')
        
        try:
            # Try to convert argument 12 to a float
            str(sys.argv[18])

        except ValueError:
            # Raise an exception if the conversion fails
            raise TypeError(f'Error: Argument at index 18 should be a string.')

        operation, number_of_operations, m, n, p, sp1, sp3 = map(int, (sys.argv[1], sys.argv[2], sys.argv[3],
                                                                       sys.argv[4], sys.argv[5], sys.argv[10],
                                                                       sys.argv[14]))

        if sys.argv[16] == "None":
            seed = None
        else:
            try:
                seed = int(sys.argv[16])
            except ValueError:
                # Raise an exception if the conversion fails
                raise ValueError(f'Invalid value for seed. It must be None or an integer.')

        c = sys.argv[6].lower() == 'true'
        lo = sys.argv[7].lower() == 'true'
        s0 = sys.argv[8].lower() == 'true'
        s1 = sys.argv[9].lower() == 'true'
        s2 = sys.argv[11].lower() == 'true'
        s3 = sys.argv[13].lower() == 'true'
        sp2 = float(sys.argv[12])
        solver = sys.argv[15]
        iteration = sys.argv[17]
        var_str = sys.argv[18]
        prev_seed = sys.argv[19]
        file_path = sys.argv[20]

        test = int(os.environ.get('test', 0))

        # Value check for operation
        if operation != 1 and operation != 0:
            raise ValueError(f'Invalid value for operation. It must be equal to 1 or 0.')

        # Specify parameters of the encoding
        encoding_str, cumulative_dict = encoding(number_of_operations, m, n, p, c, lo, s0, s1,
                                                 sp1, s2, sp2, s3, sp3, seed, iteration, var_str, prev_seed, solver)

        # Value check for encoding_str
        if len(encoding_str) < 1:
            raise ValueError("CNF instance file is empty")

        if test == 0:
            logs_path = f"logs/{number_of_operations}_{m}_{n}_{p}_{lo}_{s1}_{solver}"
        elif test == 1:
            logs_path = f"tests/logs/{number_of_operations}_{m}_{n}_{p}_{lo}_{s1}_{solver}"

        if operation:
            # Write encoding to file
            with open(file_path, "w") as file:
                file.write(encoding_str)
        else:
            # If solver outputs SAT, insert the SAT assignment
            assignment_output_string = f"{logs_path}/{number_of_operations}_{m}_{n}_{p}_{c}_{lo}" \
                                       f"_{s0}_{s1}_{sp1}_{s2}_{sp2}_{s3}_{sp3}_{solver}_{seed}_{iteration}_{var_str}/"\
                                       f"assignment_{number_of_operations}_" \
                                       f"{m}_{n}_{p}_{c}_{lo}_{s0}_{s1}_{sp1}_{s2}_{sp2}_{s3}_{sp3}_{solver}_{seed}_{iteration}_{var_str}.txt"

            with open(assignment_output_string, 'r') as file:
                assignment_string = file.read().rstrip('\n')
                if solver == "maplesat":
                    assignment_string = assignment_string[3:]

            # Removes trailing 0
            assignment_string = assignment_string[:-1]


            # Output scheme in human readable format
            scheme = scheme(assignment_string, cumulative_dict, number_of_operations, m, n, p, c)

            with open(f"{logs_path}/{number_of_operations}_{m}_{n}_{p}_{c}_{lo}" 
                      f"_{s0}_{s1}_{sp1}_{s2}_{sp2}_{s3}_{sp3}_{solver}_{seed}_{iteration}_{var_str}/"
                      f"scheme_{number_of_operations}_{m}_{n}_{p}_{c}_{lo}" 
                      f"_{s0}_{s1}_{sp1}_{s2}_{sp2}_{s3}_{sp3}_{solver}_{seed}_{iteration}_{var_str}.txt", "w") as file:
                file.write(scheme)

            # Define the file path
            file_path = (f"current_schemes/{number_of_operations}_{m}_{n}_{p}_{lo}_{s1}_{solver}/scheme_{number_of_operations}_{m}_{n}_{p}_{c}_{lo}"
                        f"_{s0}_{s1}_{sp1}_{s2}_{sp2}_{s3}_{sp3}_{solver}_{seed}_{iteration}_{var_str}.txt")

            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write to the file
            with open(file_path, "w") as file:
                file.write(scheme)

            # Perform verifications
            verifier_output = verifier(assignment_string, cumulative_dict, number_of_operations, m, n, p, c, lo, s1, solver)

            # Value check for verifier_output
            if len(str(verifier_output)) < 1:
                raise ValueError("No output by verifier 1")

            verifier_v2_output = verifier_v2(assignment_string, cumulative_dict, number_of_operations, m, n, p, c)

            # Value check for verifier_v2_output
            if len(str(verifier_v2_output)) < 1:
                raise ValueError("No output by verifier 2")

            with open(f"{logs_path}/{number_of_operations}_{m}_{n}_{p}_{c}_{lo}" 
                      f"_{s0}_{s1}_{sp1}_{s2}_{sp2}_{s3}_{sp3}_{solver}_{seed}_{iteration}_{var_str}/"
                      f"verifier_{number_of_operations}_{m}_{n}_{p}_{c}_{lo}" 
                      f"_{s0}_{s1}_{sp1}_{s2}_{sp2}_{s3}_{sp3}_{solver}_{seed}_{iteration}_{var_str}.txt", "w") as file:
                file.write(str(verifier_output))

            with open(f"{logs_path}/{number_of_operations}_{m}_{n}_{p}_{c}_{lo}" 
                      f"_{s0}_{s1}_{sp1}_{s2}_{sp2}_{s3}_{sp3}_{solver}_{seed}_{iteration}_{var_str}/"
                      f"verifier_v2_{number_of_operations}_{m}_{n}_{p}_{c}_{lo}" 
                      f"_{s0}_{s1}_{sp1}_{s2}_{sp2}_{s3}_{sp3}_{solver}_{seed}_{iteration}_{var_str}.txt", "w") as file:
                file.write(str(verifier_v2_output))

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f"An error occurred while running main: {e}")
