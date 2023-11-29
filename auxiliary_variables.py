def create_t(num_t, num_row_1, num_col_1, num_col_2, shift, var_str):
    """
    Create all t-variables representing the respective variables in Brent equations
    and map them to unique integral values using a dictionary.

    Args:
        num_t (int): Number of 't's in each Brent equation.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.
        shift (int): Current variable index offset.
        var_str (str): The string to use for variable names.

    Returns:
        dict: Dictionary of t-variables and their corresponding unique integer values.

    Notes:
        1. The values corresponding to each variable will act as the variables in the CNF file.
        2. Shift is used to ensure the values are unique, not only in their dictionary but also with respect
           to values for other variables in the encoding.
    """

    try:
        # Input validation and value checks
        # Check integer arguments and their minimum values
        for arg_name, arg_value, min_value in zip(('num_t', 'num_row_1', 'num_col_1', 'num_col_2', 'shift'),
                                                  (num_t, num_row_1, num_col_1, num_col_2, shift),
                                                  (2, 1, 1, 1, 0)):
            if not isinstance(arg_value, int):
                raise TypeError(f'The {arg_name} argument must be an integer.')

            if arg_value < min_value:
                raise ValueError(f'Invalid value for {arg_name}. It must be greater than or equal to {min_value}.')

        # Check the type of the 'var_str' argument
        if not isinstance(var_str, str):
            raise TypeError(f'The var_str argument must be a string.')

        # Check the allowed values for 'var_str'
        if var_str not in ["t", "ta", "tb"]:
            raise ValueError(f'Invalid value of var_str. It must be t, ta, or tb.')

        t_dict = {}  # Initialize an empty dictionary to store variable mappings

        # Create ranges for 't' values
        val_t_range = range(1, num_t + 1)

        # Create ranges based on the variable string
        if var_str != "ta" and var_str != "tb":
            val_i1_range = val_k1_range = range(1, num_row_1 + 1)  # Create ranges for 'i1' and 'k1' values
            val_i2_range = val_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j1' values
            val_j2_range = val_k2_range = range(1, num_col_2 + 1)  # Create ranges for 'j2' and 'k2' values

        elif var_str == "ta":
            val_i1_range = val_j1_range = val_k1_range = range(1, num_row_1 + 1)  # Create ranges for
            # 'i1', 'j1', and 'k1' values
            val_i2_range = val_j2_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j2' values
            val_k2_range = range(1, num_col_2 + 1)  # Create ranges for 'k2' values

        elif var_str == "tb":
            val_i1_range = val_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'i1' and 'j1' values
            val_i2_range = val_j2_range = val_k2_range = range(1, num_col_2 + 1)  # Create ranges for
            # 'i2', 'j2', and 'k2' values
            val_k1_range = range(1, num_row_1 + 1)  # Create ranges for 'k1' values

        index = 1  # Initialize a counter for unique integer values

        # Loop to generate t-variables and their mappings
        for val_t in val_t_range:
            for i1 in val_i1_range:
                for i2 in val_i2_range:
                    for j1 in val_j1_range:
                        for j2 in val_j2_range:
                            for k1 in val_k1_range:
                                for k2 in val_k2_range:
                                    key = f"{var_str}_{val_t}_{i1}_{i2}_{j1}_{j2}_{k1}_{k2}"  # Construct the
                                    # variable name
                                    t_dict[key] = shift + index  # Map the variable name to a unique integer value
                                    index += 1  # Increment the counter

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f"An error occurred while running 'create_t': {e}")

    return t_dict  # Return the dictionary of t-variables and their mappings


def create_s(num_t, num_row_1, num_col_1, num_col_2, shift, var_str):
    """
    Create all s-variables representing the respective variables in Brent equations
    and map them to unique integral values using a dictionary.

    Args:
        num_t (int): Number of 't's in each Brent equation.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.
        shift (int): Current variable index offset.
        var_str (str): The string to use for variable names.

    Returns:
        dict: Dictionary of 's' variables and their corresponding unique integer values.

    Notes:
        1. The values corresponding to each variable will act as the variables in the CNF file.
        2. Shift is used to ensure the values are unique, not only in their dictionary but also with respect
           to values for other variables in the encoding.
    """

    try:
        # Input validation and value checks
        # Check integer arguments and their minimum values
        for arg_name, arg_value, min_value in zip(('num_t', 'num_row_1', 'num_col_1', 'num_col_2', 'shift'),
                                                  (num_t, num_row_1, num_col_1, num_col_2, shift),
                                                  (2, 1, 1, 1, 0)):
            if not isinstance(arg_value, int):
                raise TypeError(f'The {arg_name} argument must be an integer.')

            if arg_value < min_value:
                raise ValueError(f'Invalid value for {arg_name}. It must be greater than or equal to {min_value}.')

        # Check the type of the 'var_str' argument
        if not isinstance(var_str, str):
            raise TypeError(f'The var_str argument must be a string.')

        # Check the allowed values for 'var_str'
        if var_str not in ["s", "sa", "sb"]:
            raise ValueError(f'Invalid value of var_str. It must be s, sa, or sb.')

        s_dict = {}  # Initialize an empty dictionary to store variable mappings

        # Create ranges for 't' and 'i1' values
        val_t_range = range(1, num_t + 1)
        val_i1_range = range(1, num_row_1 + 1)

        # Create ranges based on the variable string
        if var_str != "sa" and var_str != "sb":
            val_i2_range = val_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j1' values
            val_j2_range = range(1, num_col_2 + 1)  # Create a range for 'j2' values

        else:
            val_i2_range = val_j2_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j2' values
            val_j1_range = range(1, num_row_1 + 1)  # Create range for 'j1' values

        index = 1  # Initialize a counter for unique integer values

        # Loop to generate s-variables and their mappings
        for val_t in val_t_range:
            for i1 in val_i1_range:
                for i2 in val_i2_range:
                    for j1 in val_j1_range:
                        for j2 in val_j2_range:
                            key = f"{var_str}_{val_t}_{i1}_{i2}_{j1}_{j2}"  # Construct the variable name
                            s_dict[key] = shift + index  # Map the variable name to a unique integer value
                            index += 1  # Increment the counter

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f"An error occurred while running create_s: {e}")

    return s_dict  # Return the dictionary of 's' variables and their mappings
