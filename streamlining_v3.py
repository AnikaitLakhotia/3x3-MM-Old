import random
from encoding_list_v2 import at_most_two


def at_most_one(var_list, y):
    """
    Generate at-most-one constraints for a list of variables.

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
        num_aux_var = 0  # Initialize the number of auxiliary variables to y
        clause_list = []

        if num_var > 2:

            num_aux_var += 1

            # Add clauses for at most two constraints
            clause_list.extend([[-var_list[0], -var_list[1]], [-var_list[0], y], [-var_list[1], y]])

            new_var_list = [y]

            for var in var_list[2:]:
                new_var_list.append(var)

            # Recursively apply at_most_two to the remaining variables
            next_constraints, num_added_aux_var = at_most_one(new_var_list, y + 1)
            num_aux_var += num_added_aux_var

            for clause in next_constraints:
                clause_list.append(clause)

        elif num_var == 2:
            # Add clauses for at most two constraints
            clause_list.append([-var_list[0], -var_list[1]])

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f'An error occurred while running at_most_one: {e}')

    return clause_list, num_aux_var


def generate_streamlining_v3(cumulative_dict, num_var, num_t, num_row_1, num_col_1, num_col_2, num_two_terms, seed):
    """
    Generate a list of streamlining variables based on streamlining 3.

    Args:
        cumulative_dict (dict): A dict containing all the variables in the encoding(as keys) and their
                                corresponding unique integer values.
        num_var (int): Number of variables in the encoding till the function is called.
        num_t (int): Number of 't' values.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.
        num_two_terms (int): Number of two-term summands to select.

    Returns:
        list: List of streamlining variables.

    Note:
        This function generates a list of variables for streamlining by randomly selecting two terms from num_two_terms
        number of randomly selected summands and one term from the remaining summands.
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

        # Check the type of the 'num_var' argument
        if not isinstance(num_var, int):
            raise TypeError(f'The num_var argument must be an int.')

        # Check value of 'num_var' argument
        elif num_var < 0:
            raise ValueError("Invalid value for num_var argument. It must be greater than or equal to 0.")

        # Check the type of the 'num_two_terms' argument
        elif not isinstance(num_two_terms, int):
            raise TypeError(f'The num_two_terms argument must be an int.')

        # Check value of 'num_two_terms' argument
        elif num_two_terms + num_t != num_row_1 * num_col_1 * num_col_2:
            raise ValueError(f'Invalid value for num_two_terms argument. num_two_terms + {num_t} must be equal to '
                             f'{num_row_1 * num_col_1 * num_col_2}')

        # Check the type of the 'cumulative_dict' argument
        elif not isinstance(cumulative_dict, dict):
            raise TypeError(f'The cumulative_dict argument must be a string.')

        # Check length of 'cumulative_dict' argument
        elif len(cumulative_dict) < 1:
            raise ValueError(
                f'Invalid length for cumulative_dict argument. It must be greater than or equal to 1.')

        # Check the type of the 'cumulative_dict' argument
        if not isinstance(cumulative_dict, dict):
            raise TypeError(f'The cumulative_dict argument must be a dict.')

        # Check length of 'cumulative_dict' argument
        elif len(cumulative_dict) < 1:
            raise ValueError(f'Invalid length for cumulative_dict argument. It must be greater than or equal to 1.')

        # Check the allowed values for keys and values in 'cumulative_dict' argument
        for key, value in cumulative_dict.items():
            var_str = key[:2]

            if not isinstance(key, str):
                raise TypeError(f'All keys in cumulative_dict argument must be strings, found: {key}.')

            elif not isinstance(value, int):
                raise TypeError(f'All keys in cumulative_dict argument must be integers, found: {value}.')

            elif var_str not in ["aa", "a_", "bb", "b_", "g_", "s_", "sa", "sb", "t_", "ta", "tb"]:
                raise ValueError(f'Invalid key({key}) in cumulative_dict argument. It must start with'
                                 f' aa, a, bb, b, ab, ba, s, sa, sb, t, ta, or tb.')

            elif value < 1:
                raise ValueError(f'Invalid value({value}) in cumulative_dict argument. '
                                 f'It must be greater than or equal to 1')

        if len(cumulative_dict.values()) != len(set(cumulative_dict.values())):
            raise ValueError("Duplicate values found in the cumulative_dict argument.")

        val_t_range = range(1, num_t + 1)  # Create a range for 't' values
        val_i1_range = range(1, num_row_1 + 1)  # Create ranges for 'i1' values
        val_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'j1' values
        val_k2_range = range(1, num_col_2 + 1)  # Create ranges for 'k2' values

        num_aux_vars = 0
        summand_list = []
        y = num_var + 1

        # Generate summands
        for val_t in val_t_range:
            summand = []
            for i1 in val_i1_range:
                for j1 in val_j1_range:
                    for k2 in val_k2_range:
                        summand.append(cumulative_dict[f't_{val_t}_{i1}_{j1}_{j1}_{k2}_{i1}_{k2}'])
            summand_list.append(summand)

        clause_list = []

        # Set seed for random() function
        random.seed(seed)
        random.shuffle(summand_list)  # Shuffle the list of summands

        # Revert back to None(default) seed
        random.seed(None)

        num_two_terms = int(num_two_terms)
        selected_summands = summand_list[:num_two_terms]  # Select the specified number of summands
        remaining_summands = summand_list[num_two_terms:]  # The remaining summands

        for summand in selected_summands:
            at_most_two_clauses, num_added_aux_var = at_most_two(summand, y)
            for clause in at_most_two_clauses:
                clause_list.extend(clause)

            num_aux_vars += num_added_aux_var
            y += num_added_aux_var

            for i in range(len(summand)):
                negated_list = summand.copy()
                negated_list[i] = -(negated_list[i])
                clause_list.append(negated_list)

            at_least_one_clause = []
            for term in summand:
                at_least_one_clause.append(term)
            clause_list.append(at_least_one_clause)

        # Randomly sample one variable from each remaining summand
        for summand in remaining_summands:
            at_most_one_clauses, num_added_aux_var = at_most_one(summand, y)
            clause_list.extend(at_most_one_clauses)

            num_aux_vars += num_added_aux_var
            y += num_added_aux_var

            at_least_one_clause = []
            for term in summand:
                at_least_one_clause.append(term)

            clause_list.append(at_least_one_clause)

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f'An error occurred while running generate_streamlining_v3: {e}')

    return clause_list, num_aux_vars
