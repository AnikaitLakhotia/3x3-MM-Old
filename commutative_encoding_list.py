from aux_list import create_aux_list
from odd import create_odd


def create_commutative_encoding_list(cumulative_dict, num_t, num_row_1, num_col_1, num_col_2):
    """
    Generate a list of SAT encoding clauses for the commutative version of Brent equations using a
    dictionary with all named variables in the encoding along with their corresponding unique
    integer values. (the values act as the variables in the CNF file).

    Args:
        cumulative_dict (dict): A dict containing all the variables in the encoding(as keys) and their
                                corresponding unique integer values.
        num_t (int): Number of 't's.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.

    Returns:
        list: A list of clauses representing commutative encoding constraints.
    """

    # Create an empty list to store the generated clauses
    clause_list = []

    # Generate auxiliary variables based on the dimensions of matrices
    aux_list = create_aux_list(((num_row_1**2) * (num_col_2**2) * (num_col_1**2)) +
                               ((num_row_1**3) * (num_col_1**2) * num_col_2) +
                               (num_row_1 * (num_col_1**2) * (num_col_2**3)), num_t, len(cumulative_dict))
    move = 0  # Variable to track the move index for auxiliary variables

    # Iterate over the keys in cumulative_dict
    for key in cumulative_dict:
        if key.startswith("t"):
            u, v, x, y, i, j = key.split("_")[2:]
            list_var = []
            list_aux = []

            # Check if the key starts with "t_1_"
            if key.startswith("t_1_"):
                if v == x and y == j and u == i:
                    # Generate list_var and list_aux for the special case
                    for m in range(1, num_t):
                        list_var.append(cumulative_dict[f't_{m}_{u}_{v}_{x}_{y}_{i}_{j}'])
                        list_aux.append(aux_list[m - 1 + move])

                    list_var.append(cumulative_dict[f't_{num_t}_{u}_{v}_{x}_{y}_{i}_{j}'])
                    # Create odd clauses using the create_odd function
                    odd_clauses = create_odd(list_var, list_aux)
                    move += num_t - 1

                    # Add odd constraint clauses to the clause list
                    for inner_list in odd_clauses:
                        clause_list.append(inner_list)

                else:
                    # Generate list_var and list_aux for the general case
                    for m in range(1, num_t):
                        if m == 1:
                            list_var.append(-cumulative_dict[f't_{m}_{u}_{v}_{x}_{y}_{i}_{j}'])
                        else:
                            list_var.append(cumulative_dict[f't_{m}_{u}_{v}_{x}_{y}_{i}_{j}'])
                        list_aux.append(aux_list[m - 1 + move])

                    list_var.append(cumulative_dict[f't_{num_t}_{u}_{v}_{x}_{y}_{i}_{j}'])
                    # Create odd clauses using the create_odd function
                    odd_clauses = create_odd(list_var, list_aux)
                    move += num_t - 1
                    # Add odd constraint clauses to the clause list
                    for inner_list in odd_clauses:
                        clause_list.append(inner_list)

            # Check if the key starts with "ta_1_"
            elif key.startswith("ta_1_"):
                # Generate list_var and list_aux for the general case
                for m in range(1, num_t):
                    if m == 1:
                        list_var.append(-cumulative_dict[f'ta_{m}_{u}_{v}_{x}_{y}_{i}_{j}'])
                    else:
                        list_var.append(cumulative_dict[f'ta_{m}_{u}_{v}_{x}_{y}_{i}_{j}'])
                    list_aux.append(aux_list[m - 1 + move])

                list_var.append(cumulative_dict[f'ta_{num_t}_{u}_{v}_{x}_{y}_{i}_{j}'])
                # Create odd clauses using the create_odd function
                odd_clauses = create_odd(list_var, list_aux)
                move += num_t - 1
                # Add odd constraint clauses to the clause list
                for inner_list in odd_clauses:
                    clause_list.append(inner_list)

            # Check if the key starts with "tb_1_"
            elif key.startswith("tb_1_"):
                # Generate list_var and list_aux for the general case
                for m in range(1, num_t):
                    if m == 1:
                        list_var.append(-cumulative_dict[f'tb_{m}_{u}_{v}_{x}_{y}_{i}_{j}'])
                    else:
                        list_var.append(cumulative_dict[f'tb_{m}_{u}_{v}_{x}_{y}_{i}_{j}'])
                    list_aux.append(aux_list[m - 1 + move])

                list_var.append(cumulative_dict[f'tb_{num_t}_{u}_{v}_{x}_{y}_{i}_{j}'])
                # Create odd clauses using the create_odd function
                odd_clauses = create_odd(list_var, list_aux)
                move += num_t - 1
                # Add odd constraint clauses to the clause list
                for inner_list in odd_clauses:
                    clause_list.append(inner_list)

        # Check if the key starts with "s"
        elif key.startswith("s"):
            val_t, u, v, x, y = key.split("_")[1:]

            # Check if the key starts with "s_"
            if key.startswith("s_"):
                # Generate clauses for the commutative encoding constraints
                clause_list.append([-cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                    -cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                    -cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                    -cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                    -cumulative_dict[key]])
                clause_list.append([-cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                    -cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                    cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                    cumulative_dict[key]])
                clause_list.append([-cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                    -cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                    cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                    cumulative_dict[key]])
                clause_list.append([cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                    -cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                    -cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                    cumulative_dict[key]])
                clause_list.append([cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                    cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                    -cumulative_dict[key]])
                clause_list.append([cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                    cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                    -cumulative_dict[key]])
                clause_list.append([cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                    -cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                    -cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                    cumulative_dict[key]])
                clause_list.append([cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                    cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                    -cumulative_dict[key]])
                clause_list.append([cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                    cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                    -cumulative_dict[key]])

            # Check if the key starts with "sa_"
            elif key.startswith("sa_"):
                # Generate clauses for the commutative encoding constraints
                if u != x or v != y:
                    clause_list.append([-cumulative_dict[f'aa_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])
                    clause_list.append([-cumulative_dict[f'aa_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        cumulative_dict[key]])
                    clause_list.append([-cumulative_dict[f'aa_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'aa_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'aa_{val_t}_{x}_{y}'],
                                        cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'aa_{val_t}_{x}_{y}'],
                                        cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])
                else:
                    clause_list.append([-cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])

            # Check if the key starts with "sb_"
            elif key.startswith("sb_"):
                # Generate clauses for the commutative encoding constraints
                if u != x or v != y:
                    clause_list.append([-cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'bb_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])
                    clause_list.append([-cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'bb_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        cumulative_dict[key]])
                    clause_list.append([-cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'bb_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                        cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                        cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'bb_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'bb_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'bb_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])
                else:
                    clause_list.append([-cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])

    # Iterate over the keys in cumulative_dict again
    for key in cumulative_dict:
        if key.startswith("t"):
            val_t, u, v, x, y, i, j = key.split("_")[1:]

            # Check if the key starts with "t_"
            if key.startswith("t_"):
                # Generate clauses for the commutative encoding constraints for 's' and 'g' variables
                clause_list.append([-cumulative_dict[key], cumulative_dict[f's_{val_t}_{u}_{v}_{x}_{y}']])
                clause_list.append([-cumulative_dict[key], cumulative_dict[f'g_{val_t}_{i}_{j}']])
                clause_list.append([cumulative_dict[key], -cumulative_dict[f's_{val_t}_{u}_{v}_{x}_{y}'],
                                    -cumulative_dict[f'g_{val_t}_{i}_{j}']])

            # Check if the key starts with "ta_"
            elif key.startswith("ta_"):
                # Generate clauses for the commutative encoding constraints for 'sa' and 'g' variables
                clause_list.append([-cumulative_dict[key], cumulative_dict[f'sa_{val_t}_{u}_{v}_{x}_{y}']])
                clause_list.append([-cumulative_dict[key], cumulative_dict[f'g_{val_t}_{i}_{j}']])
                clause_list.append([cumulative_dict[key], -cumulative_dict[f'sa_{val_t}_{u}_{v}_{x}_{y}'],
                                    -cumulative_dict[f'g_{val_t}_{i}_{j}']])

            # Check if the key starts with "tb_"
            elif key.startswith("tb_"):
                # Generate clauses for the commutative encoding constraints for 'sb' and 'g' variables
                clause_list.append([-cumulative_dict[key], cumulative_dict[f'sb_{val_t}_{u}_{v}_{x}_{y}']])
                clause_list.append([-cumulative_dict[key], cumulative_dict[f'g_{val_t}_{i}_{j}']])
                clause_list.append([cumulative_dict[key], -cumulative_dict[f'sb_{val_t}_{u}_{v}_{x}_{y}'],
                                    -cumulative_dict[f'g_{val_t}_{i}_{j}']])

    return clause_list
