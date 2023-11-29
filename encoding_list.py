from aux_list import create_aux_list
from odd import create_odd


def create_encoding_list(cumulative_dict, num_t, num_row_1, num_col_1, num_col_2):
    """
    Create a list containing SAT encoding clauses for the first version of Brent equations using a
    dictionary with all named variables in the encoding along with their corresponding unique
    integer values. (the values act as the variables in the CNF file)

    Args:
        cumulative_dict (dict): A dict containing all the variables in the encoding(as keys) and their
                                corresponding unique integer values.
        num_t (int): Number of 't's.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.

    Returns:
        list: List of SAT encoding clauses (each clause as a list).
    """

    clause_list = []  # Initialize an empty list to store clauses
    aux_list = create_aux_list((num_row_1**2) * (num_col_2**2) * (num_col_1**2), num_t, len(cumulative_dict))
    move = 0

    for key in cumulative_dict:
        if key.startswith("t_1_"):
            val_1, val_2, val_3, val_4, val_5, val_6 = key.split("_")[2:]

            if val_2 == val_3 and val_1 == val_5 and val_4 == val_6:
                list_var = []
                list_aux = []

                for i in range(1, num_t):
                    list_var.append(cumulative_dict[f't_{i}_{val_1}_{val_2}_{val_3}_{val_4}_{val_5}_{val_6}'])
                    list_aux.append(aux_list[i - 1 + move])

                list_var.append(cumulative_dict[f't_{num_t}_{val_1}_{val_2}_{val_3}_{val_4}_{val_5}_{val_6}'])
                odd_clauses = create_odd(list_var, list_aux)
                move += num_t - 1

                # Add odd constraint clauses to the clause list
                for inner_list in odd_clauses:
                    clause_list.append(inner_list)
            else:
                list_var = []
                list_aux = []

                for i in range(1, num_t):
                    if i == 1:
                        list_var.append(-cumulative_dict[f't_{i}_{val_1}_{val_2}_{val_3}_{val_4}_{val_5}_{val_6}'])
                    else:
                        list_var.append(cumulative_dict[f't_{i}_{val_1}_{val_2}_{val_3}_{val_4}_{val_5}_{val_6}'])
                    list_aux.append(aux_list[i - 1 + move])

                list_var.append(cumulative_dict[f't_{num_t}_{val_1}_{val_2}_{val_3}_{val_4}_{val_5}_{val_6}'])
                odd_clauses = create_odd(list_var, list_aux)
                move += num_t - 1

                # Add odd constraint clauses to the clause list
                for inner_list in odd_clauses:
                    clause_list.append(inner_list)

    for key in cumulative_dict:
        # Add clauses for 's' variables
        if key.startswith("s"):
            val_t, val_1, val_2, val_3, val_4 = key.split("_")[1:]
            clause_list.append([-cumulative_dict[key], cumulative_dict[f'a_{val_t}_{val_1}_{val_2}']])
            clause_list.append([-cumulative_dict[key], cumulative_dict[f'b_{val_t}_{val_3}_{val_4}']])
            clause_list.append([cumulative_dict[key], -cumulative_dict[f'a_{val_t}_{val_1}_{val_2}'],
                                -cumulative_dict[f'b_{val_t}_{val_3}_{val_4}']])

        # Add clauses for 't' variables
        elif key.startswith("t"):
            val_t, val_1, val_2, val_3, val_4, val_5, val_6 = key.split("_")[1:]
            clause_list.append([-cumulative_dict[key], cumulative_dict[f's_{val_t}_{val_1}_{val_2}_{val_3}_{val_4}']])
            clause_list.append([-cumulative_dict[key], cumulative_dict[f'g_{val_t}_{val_5}_{val_6}']])
            clause_list.append([cumulative_dict[key], -cumulative_dict[f's_{val_t}_{val_1}_{val_2}_{val_3}_{val_4}'],
                                -cumulative_dict[f'g_{val_t}_{val_5}_{val_6}']])

    return clause_list  # Return the list of clauses
