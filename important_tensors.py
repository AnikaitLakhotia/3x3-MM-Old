import os

def scheme_list():
    """
    Reads scheme files from the 'schemes' directory.

    Returns:
        list: List of strings, each representing the contents of a scheme file.
    """

    try:
        schemes = []
        # Determine the parent directory and the 'schemes' directory path
        parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        schemes_dir = os.path.join(parent_dir, 'schemes')

        # Ensure the 'schemes' directory exists
        if not os.path.isdir(schemes_dir):
            raise FileNotFoundError(f"The 'schemes' directory was not found: {schemes_dir}")

        sub_folders = [f for f in os.listdir(schemes_dir) if os.path.isdir(os.path.join(schemes_dir, f))]

        for sub_folder in sub_folders:
            sub_folder_path = os.path.join(schemes_dir, sub_folder)

            # Ensure the subfolder exists and is a directory
            if not os.path.isdir(sub_folder_path):
                continue

            files = [f for f in os.listdir(sub_folder_path) if os.path.isfile(os.path.join(sub_folder_path, f))]
            for file in files:
                file_path = os.path.join(sub_folder_path, file)
                try:
                    with open(file_path, 'r') as file_handle:
                        file_contents = file_handle.read()
                        schemes.append(file_contents)
                except IOError as e:
                    raise IOError(f"Error reading file {file_path}: {e}")

    except Exception as e:
        raise RuntimeError(f"An error occurred while running scheme_list: {e}")

    return schemes

def important_tensors(num_t, freq_threshold):
    """
    Analyzes schemes to determine important tensors(i.e., tensors shared by many schemes) and their respective frequencies.

    Args:
        num_t (int): Number of tensors to consider.
        freq_threshold (int): The frequency threshold to determine important tensors and analyse them.

    Returns:
        list: A list containing three elements:
            - The maximum number of schemes shared by any tensor.
            - The number of tensors exceeding the frequency threshold.
            - A histogram representing the frequency distribution of tensor occurrences.
    """

    try:
        # Validate input arguments
        if not isinstance(num_t, int) or num_t <= 0:
            raise ValueError("`num_t` must be a positive integer.")
        if not isinstance(freq_threshold, int) or freq_threshold < 0:
            raise ValueError("`freq_threshold` must be a non-negative integer.")

        # Get the list of scheme contents
        schemes = scheme_list()
        bin_count_dict = {}
        bin_scheme_list = []
        bin_list = []

        for scheme in schemes:
            # Split the scheme into tensors based on the delimiter
            tensors = scheme.split('---------+---------+----------')
            tensors = tensors[:-1]  # Remove the last empty string after the split
            var_chars = ['a', 'b', 'g']  # Characters representing variable types
            var_list = []
            var_value_list = []

        # Process each tensor to extract variable values
        for tensor in tensors:
            var_lines = tensor.split('\n')
            for var_line in var_lines:
                var_sets = var_line.split('|')
                for var_set in var_sets:
                    var_group = var_set.split()
                    for var in var_group:
                        if var == '-1':
                            var_value_list.append(1)  # Convert -1 to 1
                        else:
                            var_value_list.append(int(var))  # Convert string to integer

        # Create variable representations based on extracted values
        shift = 0
        for val_t in range(1, num_t + 1):
            for i in range(1, 4):
                for var_char in var_chars:
                    for j in range(1, 4):
                        if shift < len(var_value_list):
                            if var_value_list[shift] == 1:
                                var_list.append(f'{var_char}_{val_t}_{i}_{j}')
                            else:
                                var_list.append(f'-{var_char}_{val_t}_{i}_{j}')
                            shift += 1

        # Convert variables into binary vectors and build schemes
        bin_scheme = []
        for i in range(1, num_t + 1):
            bin_vector = []
            for var in var_list:
                t = var.split("_")[1]
                if int(t) == i:
                    if var.startswith("-"):
                        bin_vector.append('0')
                    else:
                        bin_vector.append('1')

            bin_vector_str = ''.join(bin_vector)
            if bin_vector_str not in bin_list:
                bin_count_dict[bin_vector_str] = 1
                bin_list.append(bin_vector_str)
                bin_scheme.append(bin_vector_str)
            else:
                bin_count_dict[bin_vector_str] += 1
                bin_scheme.append(bin_vector_str)
        bin_scheme_list.append(bin_scheme)

        # Analyze the frequency of tensor occurrences
        max_shared_schemes = 0
        freq_count = 0
        freq_tensors = []

        for key, val in bin_count_dict.items():
            if val > max_shared_schemes:
                max_shared_schemes = val
            if val > freq_threshold:
                freq_count += 1
                freq_tensors.append(key)

        # Create a histogram for the frequency distribution of tensor occurrences
        freq_hist = [0] * num_t
        for bin_scheme in bin_scheme_list:
            num_tensors = sum(1 for key in bin_scheme if key in freq_tensors)
            if num_tensors != 0:
                freq_hist[num_tensors - 1] += 1
    
    except Exception as e:
        raise RuntimeError(f"An error occurred while running important_tensors: {e}")

    return [max_shared_schemes, freq_count, freq_hist]
