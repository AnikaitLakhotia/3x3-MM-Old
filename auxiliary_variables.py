def create_t(num_t, num_row_1, num_col_1, num_col_2, shift):
    """
    Create all t-variables (e.g., "t_1_2_1_1_3_1", "t_6_2_3_2_2_1", etc.) representing the
    respective variables in Brent equations and map them to unique integral values using a dictionary.

    Args:
        num_t (int): Number of 't's in each Brent equation.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.
        shift (int): Current variable index offset.

    Returns:
        dict: Dictionary of t-variables and their corresponding unique integer values.

    Notes:
        1. The values corresponding to each variable will act as the variables in the CNF file.
        2. Shift is used to ensure the values are unique, not only in their dictionary but also with respect
           to values for other variables in the encoding.
    """

    t_dict = {}  # Initialize an empty dictionary to store variable mappings

    val_t_range = range(1, num_t + 1)  # Create a range for 't' values
    val_i1_range = val_k1_range = range(1, num_row_1 + 1)  # Create ranges for 'i1' and 'k1' values
    val_i2_range = val_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j1' values
    val_j2_range = val_k2_range = range(1, num_col_2 + 1)  # Create ranges for 'j2' and 'k2' values

    index = 1  # Initialize a counter for unique integer values
    for val_t in val_t_range:
        for i1 in val_i1_range:
            for i2 in val_i2_range:
                for j1 in val_j1_range:
                    for j2 in val_j2_range:
                        for k1 in val_k1_range:
                            for k2 in val_k2_range:
                                key = f"t_{val_t}_{i1}_{i2}_{j1}_{j2}_{k1}_{k2}"  # Construct the variable name
                                t_dict[key] = shift + index  # Map the variable name to a unique integer value
                                index += 1  # Increment the counter

    return t_dict  # Return the dictionary of t-variables and their mappings


def create_s(num_t, num_row_1, num_col_1, num_col_2, shift):
    """
    Create all s-variables (e.g., "s_1_2_1_1", "s_6_2_3_2", etc.) representing the
    respective variables in Brent equations and map them to unique integral values using a dictionary.

    Args:
        num_t (int): Number of 't's in each Brent equation.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.
        shift (int): Current variable index offset.

    Returns:
        dict: Dictionary of 's' variables and their corresponding unique integer values.

    Notes:
        1. The values corresponding to each variable will act as the variables in the CNF file.
        2. Shift is used to ensure the values are unique, not only in their dictionary but also with respect
           to values for other variables in the encoding.
    """

    s_dict = {}  # Initialize an empty dictionary to store variable mappings

    val_t_range = range(1, num_t + 1)  # Create a range for 't' values
    val_i1_range = range(1, num_row_1 + 1)  # Create a range for 'i1' values
    val_i2_range = val_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j1' values
    val_j2_range = range(1, num_col_2 + 1)  # Create a range for 'j2' values

    index = 1  # Initialize a counter for unique integer values
    for val_t in val_t_range:
        for i1 in val_i1_range:
            for i2 in val_i2_range:
                for j1 in val_j1_range:
                    for j2 in val_j2_range:
                        key = f"s_{val_t}_{i1}_{i2}_{j1}_{j2}"  # Construct the variable name
                        s_dict[key] = shift + index  # Map the variable name to a unique integer value
                        index += 1  # Increment the counter

    return s_dict  # Return the dictionary of 's' variables and their mappings
