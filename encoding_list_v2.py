def at_most_two(var_list, y):

    num_var = len(var_list)
    num_aux_var = 2
    clause_list = []

    if num_var > 4:
        z = y + 1

        clause_list.append([[-var_list[0], -var_list[1], -var_list[2]], [-var_list[0], -var_list[1], -var_list[3]],
                            [-var_list[0], -var_list[2], -var_list[3]], [-var_list[1], -var_list[2], -var_list[3]],
                            [-var_list[0], y], [-var_list[1], y], [-var_list[0], -var_list[1], z], [-var_list[2], z],
                            [-var_list[3], z], [-var_list[2], -var_list[3], y]])

        new_var_list = [y, z]

        for var in var_list[4:]:
            new_var_list.append(var)

        next_constraints, num_added_aux_var = at_most_two(new_var_list, y + 2)
        num_aux_var += num_added_aux_var

        for clause in next_constraints:
            clause_list.append(clause)

    elif num_var == 4:
        clause_list.append([[-var_list[0], -var_list[1], -var_list[2]], [-var_list[0], -var_list[1], -var_list[3]],
                            [-var_list[0], -var_list[2], -var_list[3]], [-var_list[1], -var_list[2], -var_list[3]]])

    else:
        clause_list.append([[-var_list[0], -var_list[1]], [-var_list[0], -var_list[2]],
                            [-var_list[1], -var_list[2]]])

    return clause_list, num_aux_var


def create_encoding_list_v2(cumulative_dict, num_row_1, num_col_1, num_col_2):

    num_aux_var = 0
    clause_list = []  # Initialize an empty list to store clauses

    val_i1_range = val_k1_range = range(1, num_row_1 + 1)  # Create ranges for 'i1' and 'k1' values
    val_i2_range = val_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j1' values
    val_j2_range = val_k2_range = range(1, num_col_2 + 1)  # Create ranges for 'j2' and 'k2' values

    for i1 in val_i1_range:
        for i2 in val_i2_range:
            for j1 in val_j1_range:
                for j2 in val_j2_range:
                    for k1 in val_k1_range:
                        for k2 in val_k2_range:
                            list_var = []

                            for key, value in cumulative_dict.items():
                                if key.endswith(f'{i1}_{i2}_{j1}_{j2}_{k1}_{k2}'):
                                    list_var.append(value)

                            for i in range(len(list_var)):
                                negated_list = list_var.copy()
                                negated_list[i] = -negated_list[i]
                                clause_list.append(negated_list)

                            y = len(cumulative_dict) + 1
                            at_most_two_clauses, num_added_aux_var = at_most_two(list_var, y)
                            num_aux_var += num_added_aux_var
                            for list_clause in at_most_two_clauses:
                                for clause in list_clause:
                                    clause_list.append(clause)
    return clause_list, num_aux_var  # Return the list of clauses
