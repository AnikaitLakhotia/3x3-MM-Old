from verifier import reverse_map


def scheme(sat_assignment, cumulative_dict, num_t, num_row_1, num_col_1, num_col_2, commutative):
    """
    Convert sat_assignment to scheme in human-readable format.

    Args:
    sat_assignment (str): A space-separated string of values.
    cumulative_dict (dict): A dictionary mapping keys to values.
    num_t (int): Number of 't's.
    num_row_1 (int): Number of rows in the first matrix.
    num_col_1 (int): Number of columns in the first matrix.
    num_col_2 (int): Number of columns in the second matrix.
    commutative (bool): Commutative encoding is used if True and non-commutative if False.

    Returns:
    - str: Formatted output string representing the scheme results.
    """
    try:
        horizontal_length = max(num_col_1, num_col_2)
        vertical_length = max(num_row_1, num_col_1)
        result = reverse_map(sat_assignment, cumulative_dict)  # Apply reverse_map to get result
        out_list = []  # Initialize an empty list to store output lines

        # Iterate over time steps (t), rows (i), and variables (var)
        for t in range(1, num_t + 1):
            for i in range(1, horizontal_length + 1):
                var_list = ['a', 'b', 'g']
                # Iterate over variables 'a', 'b', 'g' for each row (i)
                for var in var_list:
                    # Iterate over columns (j) for each variable (var) and row (i)
                    for j in range(1, vertical_length + 1):
                        if f"{var}_{t}_{i}_{j}" in result:
                            out_list.append(f'{result[f"{var}_{t}_{i}_{j}"]} ')  # Append formatted result
                        else:
                            out_list.append("  ")
                    if var != 'g':
                        out_list.append("| ")  # Add separator "|" except for 'g'
                out_list.append("\n")  # Add newline at the end of each row
            
            out_list.append(3*(horizontal_length**2)*"-")  # Add a horizontal line after each time step
            if t < num_t:
                out_list.append("\n")  # Add newline if not the last time step

        # Join all elements in out_list into a single string
        out = ''.join([' '.join(map(str, innerlist)) for innerlist in out_list])
        return out  # Return the final output string

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f'An error occurred while running scheme: {e}')