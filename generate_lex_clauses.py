def generate_lex_encoding(vector_1, vector_2, num_var):
    """
    Generate the lexicographical ordering clauses for a SAT problem.

    Args:
        vector_1 (list): List of variables for the first vector.
        vector_2 (list): List of variables for the second vector.
        num_var (int): Current variable index offset.

    Returns:
        tuple: A tuple containing the encoding string, the number of auxiliary variables, and the number of clauses.

    Note:
        The function generates lexicographical ordering clauses that give vector 1 a
        higher lex order to lexicographical order relative to vector 2.

    """

    try:
        # Input validation and value checks
        for arg_name, arg_value in zip(('vector_1', 'vector_2'),
                                       (vector_1, vector_2)):
            if not isinstance(arg_value, list):
                raise TypeError(f'The {arg_name} argument must be a list')

            elif len(arg_value) < 1:
                raise ValueError(f'Invalid length for {arg_name} argument. It must be greater than or equal to 1.')

            elif len(arg_value) != len(set(arg_value)):
                raise ValueError(f'Duplicate values found in the {arg_name} argument.')

            # Input validation and value checks for elements of vector argument
            for element in arg_value:
                if not isinstance(element, int):
                    raise TypeError(f'All elements in {arg_name} argument must be integers, found: {element}.')

        if not isinstance(num_var, int):
            raise TypeError(f'The num_var argument must be an int.')

        elif num_var < 0:
            raise ValueError(f'Invalid value for num_var argument. It must be greater than or equal to 0.')

        encoding_string = ""
        encoding_list = []
        num_aux_var = len(vector_1) - 1  # Calculate the number of auxiliary variables

        # Add initial clauses to encoding_string
        encoding_string += (
            f'-{vector_1[0]} {vector_2[0]} -{num_var + 1} 0 \n'
            f'{vector_1[0]} -{vector_2[0]} -{num_var + 1} 0 \n'
            f'-{vector_1[0]} -{vector_2[0]} {num_var + 1} 0 \n'
            f'{vector_1[0]} {vector_2[0]} {num_var + 1} 0 \n'
        )

        encoding_string += (f'{vector_1[0]} -{vector_2[0]} 0 \n')

        # Loop through auxiliary variables and add clauses to encoding_list
        for i in range(1, num_aux_var):
            aux_var = i + num_var
            encoding_list += [
                f'-{vector_1[i]} -{vector_2[i]} -{aux_var} {aux_var + 1} 0 \n',
                f'-{vector_1[i]} {vector_2[i]} -{aux_var + 1} 0 \n',
                f'{vector_1[i]} -{vector_2[i]} -{aux_var + 1} 0 \n',
                f'{vector_1[i]} {vector_2[i]} -{aux_var} {aux_var + 1} 0 \n',
                f'{aux_var} -{aux_var + 1} 0 \n',
            ]

        # Add clauses for auxiliary variables
        for i in range(1, num_aux_var + 1):
            aux_var = i + num_var
            encoding_list += [f'{vector_1[i]} -{vector_2[i]} -{aux_var} 0 \n']
            encoding_list += [f'-{vector_1[i]} {aux_var} 0 \n']
            encoding_list += [f'{vector_2[i]} {aux_var} 0 \n']

        encoding_string += "".join(encoding_list)

        num_clauses = encoding_string.count(' 0 \n')

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f'An error occurred while running generate_lex_encoding: {e}')

    return encoding_string, num_aux_var, num_clauses


def generate_var_list(num_t, num_row_1, num_col_1, num_col_2, cumulative_dict, commutative):
    """
    Generate vectors for lex ordering.

    Args:
        num_t (int): Number of 't's.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.
        cumulative_dict (dict): A dict containing all the variables in the encoding(as keys) and their
                                corresponding unique integer values.
        commutative (bool): Commutative encoding is used if True and non-commutative if False.

    Returns:
        tuple: A tuple containing two lists - 'vectors_col_wise' and 'vectors_row_wise'.

    Notes:
        The function generates lists containing row-wise and column-wise vectors.

    """

    try:
        # Input validation and value checks
        for arg_name, arg_value, min_value in zip(('num_t', 'num_row_1', 'num_col_1', 'num_col_2'),
                                                  (num_t, num_row_1, num_col_1, num_col_2),
                                                  (2, 1, 1, 1)):
            if not isinstance(arg_value, int):
                raise TypeError(f'The {arg_name} argument must be an integer.')

            elif arg_value < min_value:
                raise ValueError(f'Invalid value for {arg_name}. It must be greater than or equal to {min_value}.')

            # Check the type of the 'cumulative_dict' argument
            elif not isinstance(cumulative_dict, dict):
                raise TypeError(f'The cumulative_dict argument must be a dict.')

        # Check length of 'cumulative_dict' argument
        if len(cumulative_dict) < 1:
            raise ValueError(
                f'Invalid length for cumulative_dict argument. It must be greater than or equal to 1.')

        # Check the allowed values for keys and values in 'cumulative_dict' argument
        for key, value in cumulative_dict.items():
            var_str = key[:2]

            if not isinstance(key, str):
                raise TypeError(f'All keys in cumulative_dict argument must be strings, found: {key}.')

            elif not isinstance(value, int):
                raise TypeError(f'All keys in cumulative_dict argument must be integers, found: {value}.')

            elif var_str not in ["aa", "a_", "bb", "b_", "ab", "ba", "g_", "s_", "sa", "sb", "t_", "ta", "tb"]:
                raise ValueError(f'Invalid key({key}) in cumulative_dict argument. It must start with'
                                 f' aa, a, bb, b, ab, ba, s, sa, sb, t, ta, or tb.')

            elif value < 1:
                raise ValueError(f'Invalid value({value}) in cumulative_dict argument. '
                                 f'It must be greater than or equal to 1')

        if len(cumulative_dict.values()) != len(set(cumulative_dict.values())):
            raise ValueError("Duplicate values found in the cumulative_dict argument.")

        # Input validation for commutative argument
        if not isinstance(commutative, bool):
            raise TypeError(f'The commutative argument must be a bool.')

        vectors_col_wise = []
        vectors_row_wise = []
        val_t_range = range(1, num_t + 1)  # Create a range for 't' values
        val_i1_range = val_k1_range = range(1, num_row_1 + 1)  # Create ranges for 'i1' and 'k1' values
        val_i2_range = val_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j1' values
        val_j2_range = val_k2_range = range(1, num_col_2 + 1)  # Create ranges for 'j2' and 'k2' values

        if not commutative:
            # Generate column-wise vectors
            for val_t in val_t_range:
                vector = []
                prefixes = [f'a_{val_t}_', f'b_{val_t}_', f'g_{val_t}_']
                for var, value in cumulative_dict.items():
                    if any(var.startswith(prefix) for prefix in prefixes):
                        vector.append(value)
                vectors_col_wise.append(vector)

            # Generate row-wise vectors
            for i1 in val_i1_range:
                for i2 in val_i2_range:
                    for j1 in val_j1_range:
                        for j2 in val_j2_range:
                            for k1 in val_k1_range:
                                for k2 in val_k2_range:
                                    vector = []
                                    for var, value in cumulative_dict.items():
                                        if ((var.startswith('a_') and var.endswith(f'{i1}_{i2}')) or
                                                (var.startswith('b_') and var.endswith(f'{j1}_{j2}')) or
                                                (var.startswith('g_') and var.endswith(f'{k1}_{k2}'))):
                                            vector.append(value)
                                    vectors_row_wise.append(vector)

        elif commutative:
            # Generate column-wise vectors
            for val_t in val_t_range:
                vector = []
                prefixes = [f'aa_{val_t}_', f'bb_{val_t}_', f'g_{val_t}_', f'ab_{val_t}_', f'ba_{val_t}_']
                for var, value in cumulative_dict.items():
                    if any(var.startswith(prefix) for prefix in prefixes):
                        vector.append(value)
                vectors_col_wise.append(vector)

            # Generate row-wise vectors
            for i1 in val_i1_range:
                for i2 in val_i2_range:
                    for j1 in val_j1_range:
                        for j2 in val_j2_range:
                            for k1 in val_k1_range:
                                for k2 in val_k2_range:
                                    vector = []
                                    for var, value in cumulative_dict.items():
                                        if ((var.startswith('aa_') and var.endswith(f'{i1}_{i2}')) or
                                                (var.startswith('bb_') and var.endswith(f'{j1}_{j2}')) or
                                                (var.startswith('g_') and var.endswith(f'{k1}_{k2}')) or
                                                (var.startswith('ab_') and var.endswith(f'{j1}_{j2}')) or
                                                (var.startswith('ba_') and var.endswith(f'{i1}_{i2}'))):
                                            vector.append(value)
                                    vectors_row_wise.append(vector)

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f'An error occurred while running generate_var_list: {e}')
    return vectors_col_wise, vectors_row_wise
