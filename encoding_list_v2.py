from aux_list import create_aux_list
from odd import create_odd


def at_most_two(var_list, y):
    """
            Generate at-most-two constraints for a list of variables.

            Args:
                var_list (list): List of variables to apply the constraints to.
                y (int): A unique variable index for auxiliary variables.

            Returns:
                tuple: A tuple containing a list of clauses and the number of auxiliary variables added.
            """

    try:
        # Input validation and value checks for 'y' argument
        if not isinstance(y, int):
            raise TypeError('The y argument must be an integer.')

        if y < 1:
            raise ValueError(f'Invalid value for y. It must be greater than or equal to 1.')

        # Input validation and value checks for 'var_list' argument
        if not isinstance(var_list, list):
            raise TypeError('The list argument must be an integer.')

        if len(var_list) < 1:
            raise ValueError(f'Invalid length of var_list. It must be greater than or equal to 1.')

        for var in var_list:
            if not isinstance(var, int):
                raise TypeError(f'Found invalid variable({var}) in var_list. '
                                f'It must be an integer')
        if len(var_list) != len(set(var_list)):
            raise ValueError("Duplicate values found in the cumulative_dict argument.")

        num_var = len(var_list)
        num_aux_var = 2  # Initialize the number of auxiliary variables to 2
        clause_list = []

        if num_var > 4:
            z = y + 1

            # Add clauses for at most two constraints
            clause_list.append([[-var_list[0], -var_list[1], -var_list[2]], [-var_list[0], -var_list[1], -var_list[3]],
                                [-var_list[0], -var_list[2], -var_list[3]], [-var_list[1], -var_list[2], -var_list[3]],
                                [-var_list[0], y], [-var_list[1], y], [-var_list[0], -var_list[1], z],
                                [-var_list[2], z], [-var_list[3], z], [-var_list[2], -var_list[3], y]])

            new_var_list = [y, z]

            for var in var_list[4:]:
                new_var_list.append(var)

            # Recursively apply at_most_two to the remaining variables
            next_constraints, num_added_aux_var = at_most_two(new_var_list, y + 2)
            num_aux_var += num_added_aux_var

            for clause in next_constraints:
                clause_list.append(clause)

        elif num_var == 4:
            # Add clauses for at most two constraints
            clause_list.append([[-var_list[0], -var_list[1], -var_list[2]], [-var_list[0], -var_list[1], -var_list[3]],
                                [-var_list[0], -var_list[2], -var_list[3]], [-var_list[1], -var_list[2], -var_list[3]]])

        else:
            # Add clauses for at most two constraints
            clause_list.append([[-var_list[0], -var_list[1], -var_list[2]]])

        return clause_list, num_aux_var

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f'An error occurred while running at_most_two: {e}')


def create_encoding_list_v2(cumulative_dict, num_t, num_row_1, num_col_1, num_col_2):
    """
        Generate a list of SAT encoding clauses for the second version of Brent equations using a
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
            tuple: A tuple containing a list of clauses (each clause as a list) and
            the number of auxiliary variables added.
        """

    try:
        # Input validation and value checks
        for arg_name, arg_value, min_value in zip(('num_t', 'num_row_1', 'num_col_1', 'num_col_2'),
                                                  (num_t, num_row_1, num_col_1, num_col_2),
                                                  (2, 1, 1, 1)):
            if not isinstance(arg_value, int):
                raise TypeError(f'The {arg_name} argument must be an integer.')

            if arg_value < min_value:
                raise ValueError(f'Invalid value for {arg_name}. It must be greater than or equal to {min_value}.')

        # Check length of 'cumulative_dict' argument
        if len(cumulative_dict) < 1:
            raise ValueError(f'Invalid length for cumulative_dict argument. It must be greater than or equal to 1.')

        # Check the allowed values for keys and values in 'cumulative_dict' argument
        for key, value in cumulative_dict.items():
            if not isinstance(key, str):
                raise TypeError(f'All keys in cumulative dict argument must be strings, found: {key}.')
            if not isinstance(value, int):
                raise TypeError(f'All keys in cumulative dict argument must be integers, found: {value}.')
            var_str = key[0]
            if var_str not in ["a", "b", "g", "s", "t"]:
                raise ValueError(f'Invalid key({key}) in cumulative_dict argument. It must start with'
                                 f'be a, b, g, s or t.')
            if value < 1:
                raise ValueError(f'Invalid value({value}) in cumulative_dict argument. '
                                 f'It must be greater than or equal to 1')
            if len(cumulative_dict.values()) != len(set(cumulative_dict.values())):
                raise ValueError("Duplicate values found in the cumulative_dict argument.")

            # Auxiliary variables for the cases in which i2 != j1 or k1 != i1 or k2 != j2.
            num_aux_var = 0

            # List of auxiliary variables for the cases in which i2 == j1 and k1 == i1 and k2 == j2.
            aux_list = create_aux_list(num_row_1 * num_col_2 * num_col_1,
                                       num_t, len(cumulative_dict))
            move = 0
            clause_list = []

            val_i1_range = val_k1_range = range(1, num_row_1 + 1)  # Create ranges for 'i1' and 'k1' values
            val_i2_range = val_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j1' values
            val_j2_range = val_k2_range = range(1, num_col_2 + 1)  # Create ranges for 'j2' and 'k2' values

            y = len(cumulative_dict) + 1

            for i1 in val_i1_range:
                for i2 in val_i2_range:
                    for j1 in val_j1_range:
                        for j2 in val_j2_range:
                            for k1 in val_k1_range:
                                for k2 in val_k2_range:
                                    list_var = []

                                    if i2 != j1 or k2 != j2 or k1 != i1:
                                        for key, value in cumulative_dict.items():
                                            if key.endswith(f'{i1}_{i2}_{j1}_{j2}_{k1}_{k2}'):
                                                list_var.append(value)

                                        # Generate clauses with one variable negated for all such
                                        # combinations of variables
                                        for i in range(len(list_var)):
                                            negated_list = list_var.copy()
                                            negated_list[i] = -(negated_list[i])
                                            clause_list.append(negated_list)

                                        at_most_two_clauses, num_added_aux_var = at_most_two(list_var, y)
                                        y += num_added_aux_var
                                        num_aux_var += num_added_aux_var

                                        # Add at most two constraints to the clause list
                                        for list_clause in at_most_two_clauses:
                                            for clause in list_clause:
                                                clause_list.append(clause)

                                    else:
                                        list_aux = []

                                        for i in range(1, num_t):
                                            list_var.append(
                                                cumulative_dict[f't_{i}_{i1}_{i2}_{j1}_{j2}_{k1}_{k2}'])
                                            list_aux.append(aux_list[i - 1 + move])

                                        list_var.append(
                                            cumulative_dict[f't_{num_t}_{i1}_{i2}_{j1}_{j2}_{k1}_{k2}'])
                                        odd_clauses = create_odd(list_var, list_aux)
                                        move += num_t - 1

                                        # Add odd constraint clauses to the clause list
                                        for inner_list in odd_clauses:
                                            clause_list.append(inner_list)

            # Add clauses for 's' variables
            for key in cumulative_dict:
                if key.startswith("s"):
                    val_t, val_1, val_2, val_3, val_4 = key.split("_")[1:]
                    clause_list.append([-cumulative_dict[key], cumulative_dict[f'a_{val_t}_{val_1}_{val_2}']])
                    clause_list.append([-cumulative_dict[key], cumulative_dict[f'b_{val_t}_{val_3}_{val_4}']])
                    clause_list.append([cumulative_dict[key], -cumulative_dict[f'a_{val_t}_{val_1}_{val_2}'],
                                        -cumulative_dict[f'b_{val_t}_{val_3}_{val_4}']])

            # Add clauses for 't' variables
            for key in cumulative_dict:
                if key.startswith("t"):
                    val_t, val_1, val_2, val_3, val_4, val_5, val_6 = key.split("_")[1:]
                    clause_list.append(
                        [-cumulative_dict[key], cumulative_dict[f's_{val_t}_{val_1}_{val_2}_{val_3}_{val_4}']])
                    clause_list.append([-cumulative_dict[key], cumulative_dict[f'g_{val_t}_{val_5}_{val_6}']])
                    clause_list.append(
                        [cumulative_dict[key], -cumulative_dict[f's_{val_t}_{val_1}_{val_2}_{val_3}_{val_4}'],
                         -cumulative_dict[f'g_{val_t}_{val_5}_{val_6}']])

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f'An error occurred while running create_encoding_list_v2: {e}')

    return clause_list, num_aux_var
