import os
import random


class SchemeError(Exception):
    pass


def get_scheme():
    """
    Retrieve a random scheme from the 'schemes' directory.

    Returns:
        str: The contents of a random scheme file.
    """

    try:
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

        # Choose a random sub folder within 'schemes'
        random_sub_folder = random.choice(sub_folders)

        # Navigate to the randomly chosen sub folder
        sub_folder_path = os.path.join(schemes_dir, random_sub_folder)

        # Get a list of files within the randomly chosen sub folder
        files = [f for f in os.listdir(sub_folder_path) if os.path.isfile(os.path.join(sub_folder_path, f))]

        if not files:
            raise SchemeError("No files found in the randomly chosen sub folder.")

        # Choose a random file from the sub folder
        random_file = random.choice(files)

        # Read the contents of the randomly chosen file into a string
        file_path = os.path.join(sub_folder_path, random_file)
        with open(file_path, 'r') as file:
            file_contents = file.read()

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f'An error occurred while running get_scheme: {e}')

    return file_contents


def generate_streamlining_v1():
    """
    Generate a list of streamlining variables based on streamlining 1.

    Returns:
        list: List of variables.

    Note:
        This function generates a list of variables for streamlining based on the contents of a random scheme file.
    """

    file_contents = get_scheme()
    tensors = file_contents.split('---------+---------+----------')
    tensors = tensors[:-1]
    var_chars = ['a', 'b', 'g']
    var_list = []
    var_value_list = []

    # Process the scheme file
    for tensor in tensors:
        var_lines = tensor.split('\n')
        for var_line in var_lines:
            var_sets = var_line.split('|')
            for var_set in var_sets:
                var_group = var_set.split()
                for var in var_group:
                    if var == '-1':
                        var_value_list.append(1)
                    else:
                        var_value_list.append(int(var))

    shift = 0
    for val_t in range(1, 24):
        for i in range(1, 4):
            for var_char in var_chars:
                for j in range(1, 4):
                    if var_value_list[shift] == 1:
                        var_list.append(f'{var_char}_{val_t}_{i}_{j}')
                    else:
                        var_list.append(f'-{var_char}_{val_t}_{i}_{j}')
                    shift += 1

    # Switch indices of gamma variables
    modified_var_list = []
    for var in var_list:
        if var.startswith("g") or var.startswith("-g"):
            var_str, val_t, i, j = var.split("_")
            modified_var_list.append(f'{var_str}_{val_t}_{j}_{i}')
        else:
            modified_var_list.append(var)

    return modified_var_list
