import os
import random


class SchemeError(Exception):
    pass


def get_scheme():
    try:
        # Navigate to one level above the current directory
        parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

        # Navigate to 'schemes' within the parent directory
        schemes_dir = os.path.join(parent_dir, 'schemes')

        if not os.path.exists(schemes_dir) or not os.path.isdir(schemes_dir):
            raise SchemeError("'schemes' doesn't exist in the parent directory.")

        # Get a list of subdirectories (folders) inside 'schemes'
        subfolders = [f for f in os.listdir(schemes_dir) if os.path.isdir(os.path.join(schemes_dir, f))]

        if not subfolders:
            raise SchemeError("No subfolders found within 'schemes'.")

        # Choose a random subfolder within 'schemes'
        random_subfolder = random.choice(subfolders)

        # Navigate to the randomly chosen subfolder
        subfolder_path = os.path.join(schemes_dir, random_subfolder)

        # Get a list of files within the randomly chosen subfolder
        files = [f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))]

        if not files:
            raise SchemeError("No files found in the randomly chosen subfolder.")

        # Choose a random file from the subfolder
        random_file = random.choice(files)

        # Read the contents of the randomly chosen file into a string
        file_path = os.path.join(subfolder_path, random_file)
        with open(file_path, 'r') as file:
            file_contents = file.read()

        return file_contents
    except SchemeError as e:
        return str(e)


def generate_streamlining_v1():

    file_contents = get_scheme()
    tensors = file_contents.split('---------+---------+----------')
    var_chars = ['a', 'b', 'g']
    var_list = []
    var_value_list = []
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
    return var_list



