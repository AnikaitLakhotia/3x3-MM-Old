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
    encoding_string = ""
    encoding_list = []
    num_aux_var = len(vector_1) - 1  # Calculate the number of auxiliary variables

    # Add initial clauses to encoding_string
    encoding_string += (
        f'-{vector_1[0]} {vector_2[0]} {num_var + 1} 0 \n'
        f'{vector_1[0]} -{vector_2[0]} {num_var + 1} 0 \n'
        f'{vector_1[0]} {vector_2[0]} -{num_var + 1} 0 \n'
        f'{vector_1[0]} {vector_2[0]} {num_var + 1} 0 \n'
    )

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
        encoding_list += [f'-{vector_1[i]} {vector_2[i]} -{aux_var} 0 \n']

    encoding_string = "".join(encoding_list)

    num_clauses = encoding_string.count(' 0 \n')

    return encoding_string, num_aux_var, num_clauses


def generate_var_list(num_t, num_row_1, num_col_1, num_col_2, cumulative_dict):
    """
    Generate vectors for lex ordering.

    Args:
        num_t (int): Number of 't's.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.
        cumulative_dict (dict): A dict containing all the variables in the encoding(as keys) and their
                                corresponding unique integer values.

    Returns:
        tuple: A tuple containing two lists - 'vectors_col_wise' and 'vectors_row_wise'.

    Notes:
        The function generates lists containing row-wise and column-wise vectors.

    """
    vectors_col_wise = []
    vectors_row_wise = []
    val_t_range = range(1, num_t + 1)  # Create a range for 't' values
    val_i1_range = val_k1_range = range(1, num_row_1 + 1)  # Create ranges for 'i1' and 'k1' values
    val_i2_range = val_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j1' values
    val_j2_range = val_k2_range = range(1, num_col_2 + 1)  # Create ranges for 'j2' and 'k2' values

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

    return vectors_col_wise, vectors_row_wise
