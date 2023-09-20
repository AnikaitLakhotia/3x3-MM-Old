from encoding import encoding
from verifier import verifier
if __name__ == '__main__':

    # Specify parameters of the encoding
    encoding, cumulative_dict = encoding(6, 2, 2, 4)

    # Insert the path to the file where the cnf formula is to be stored
    file_path = "your_file_path"

    # Open file and write data to it
    with open(file_path, "w") as file:
        file.write(encoding)

    # If solver outputs SAT, insert the SAT assignment
    assignment_string = "insert_assignment_if_sat"

    # Print verification result
    print(verifier(assignment_string, cumulative_dict, 6))
