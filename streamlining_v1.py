import os
import random
import re


class SchemeError(Exception):
    pass


def get_scheme(num_t, num_row_1, num_col_1, num_col_2, seed, prev_seed, var_str):
    """
    Retrieve a random scheme from the 'schemes' directory if seed is not zero. 

    Args:
        num_t (int): Number of 't's.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.
        seed (None or int): Seed for random() function.
        var_str (str): The type of variables to streamline.
        prev_seed (int): Index of the scheme file to retrieve, used to select a specific scheme file if 
            `var_str` is not "n".

    Returns:
        str: The contents of a random scheme file.
    """

    try:
         # Input validation and value check for seed
        if seed is not None:
            try:
                int(seed)
            except ValueError:
                # Raise an exception if the conversion fails
                raise ValueError(f'Invalid value for seed. It must be None or an integer.')

        if var_str != "n":
            # Get the current working directory
            current_dir = os.getcwd()

            # Navigate to 'logs' within the current directory
            schemes_dir = os.path.join(current_dir, 'schemes')

            # Get the list of files in the directory
            files = os.listdir(schemes_dir)

            # Sort the files
            files.sort()

            if 0 <= int(prev_seed)-1 < len(files):
                # Get the nth file name
                nth_file = files[int(prev_seed)-1]
            
                # Create the full file path
                file_path = os.path.join(schemes_dir, nth_file)
                
                # Open and read the file
                with open(file_path, 'r') as file:
                    file_contents = file.read()
                
            else:
                print(f"No {int(prev_seed)}th file in the directory")

        else:
            # Navigate to one level above the current directory
            parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

            # Navigate to 'schemes' within the parent directory
            schemes_dir = os.path.join(parent_dir, 'schemes')

            if not os.path.exists(schemes_dir) or not os.path.isdir(schemes_dir):
                raise SchemeError("'schemes' doesn't exist in the parent directory.")

            # Get a list of subdirectories (folders) inside 'schemes'
            sub_folders = [f for f in os.listdir(schemes_dir) if os.path.isdir(os.path.join(schemes_dir, f))]

            if not sub_folders:
                raise SchemeError("No sub folders found within 'schemes'.")

            # Set seed for random() function
            random.seed(seed)

            # Choose a random sub folder within 'schemes'
            random_sub_folder = random.choice(sub_folders)

            # Revert back to None(default) seed
            random.seed(None)

            # Navigate to the randomly chosen sub folder
            sub_folder_path = os.path.join(schemes_dir, random_sub_folder)

            # Get a list of files within the randomly chosen sub folder
            files = [f for f in os.listdir(sub_folder_path) if os.path.isfile(os.path.join(sub_folder_path, f))]

            if not files:
                raise SchemeError("No files found in the randomly chosen sub folder.")

            #Set seed for random() function
            random.seed(seed)

            # Choose a random file from the sub folder
            random_file = random.choice(files)

            # Revert back to None(default) seed
            random.seed(None)

            # Read the contents of the randomly chosen file into a string
            file_path = os.path.join(sub_folder_path, random_file)
            with open(file_path, 'r') as file:
                file_contents = file.read()

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f'An error occurred while running get_scheme: {e}')

    return file_contents


def generate_streamlining_v1(num_t, num_row_1, num_col_1, num_col_2, seed, var_str, prev_seed):
    """
    Generate a list of streamlining variables based on streamlining 1.

    Args:
        num_t (int): Number of 't's.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.
        seed (None or int): Seed for random() function.
        var_str (str): The type of variables to streamline.
        prev_seed (int): Index of the scheme file to retrieve, used to select a specific scheme file if 
            `var_str` is not "n".

    Returns:
        list: List of variables.

    Note:
        This function generates a list of variables for streamlining based on the contents of a random scheme file.
    """

    # Input validation and value check for seed
    if seed is not None:
        try:
            int(seed)
        except ValueError:
            # Raise an exception if the conversion fails
            raise ValueError(f'Invalid value for seed. It must be None or an integer.')

    # Retrieve the contents of the scheme file using the get_scheme function
    file_contents = get_scheme(num_t, num_row_1, num_col_1, num_col_2, seed, prev_seed, var_str)

    # Split the contents of the scheme file into separate tensors
    tensors = re.split(r'-+', file_contents)
    
    # Exclude the last empty split result
    tensors = tensors[:-1]
    
    # Define variable characters used for generating variables
    var_chars = ['a', 'b', 'g']
    
    # Initialize lists to store variable names and their corresponding values
    var_list = []
    var_value_list = []

    # Process each tensor from the scheme file
    for tensor in tensors:
        # Split the tensor into individual lines
        var_lines = tensor.split('\n')
        for var_line in var_lines:
            # Split each line into variable sets
            var_sets = var_line.split('|')
            for var_set in var_sets:
                # Split each set into individual variables
                var_group = var_set.split()
                for var in var_group:
                    # Append variable values to the list; convert '-1' to 1
                    if var == '-1':
                        var_value_list.append(1)
                    else:
                        var_value_list.append(int(var))

    # Initialize a shift variable to track the current position in var_value_list
    shift = 0

    # Generate variables based on the processed scheme and input parameters
    for val_t in range(1, num_t + 1):
        for i in range(1, max(num_row_1, num_col_1) + 1):
            for var_char in var_chars:
                for j in range(1, max(num_col_1, num_col_2) + 1):
                    # Check conditions based on the current character and matrix dimensions
                    if (var_char == "a" and i < num_row_1 + 1 and j < num_col_1 + 1) or \
                       (var_char == "b" and i < num_col_1 + 1 and j < num_col_2 + 1) or \
                       (var_char == "g" and i < num_row_1 + 1 and j < num_col_2 + 1):
                        # Append variables to the list based on the values and var_str condition
                        if var_value_list[shift] == 1 and (var_str == "n" or var_char == var_str):
                            var_list.append(f'{var_char}_{val_t}_{i}_{j}')
                        elif var_str == "n" or var_char == var_str:
                            var_list.append(f'-{var_char}_{val_t}_{i}_{j}')
                        # Increment the shift counter to move to the next value
                        shift += 1

    return var_list