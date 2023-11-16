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

    num_var = len(var_list)
    num_aux_var = 1  # Initialize the number of auxiliary variables to 1y
    clause_list = []

    if num_var > 2:

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
    return clause_list, num_aux_var

def generate_streamlining_v3(cumulative_dict, num_var, num_t, num_row_1, num_col_1, num_two_terms):
    """
    Generate a list of streamlining variables based on streamlining 3.

    Args:
        cumulative_dict (dict): A dict containing all the variables in the encoding(as keys) and their
                                corresponding unique integer values.
        num_var (int): Number of variables in the encoding till the function is called.
        num_t (int): Number of 't' values.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_two_terms (int): Number of two-term summands to select.

    Returns:
        list: List of streamlining variables.

    Note:
        This function generates a list of variables for streamlining by randomly selecting two terms from num_two_terms
        number of randomly selected summands and one term from the remaining summands.
    """

    val_t_range = range(1, num_t + 1)  # Create a range for 't' values
    val_i1_range = val_k1_range = range(1, num_row_1 + 1)  # Create ranges for 'i1' and 'k1' values
    val_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j1' values

    num_aux_vars = 1
    summand_list = []
    y = num_var

    # Generate summands
    for val_t in val_t_range:
        summand = []
        for i1 in val_i1_range:
            for j1 in val_j1_range:
                for k1 in val_k1_range:
                    summand.append(cumulative_dict[f't_{val_t}_{i1}_{j1}_{j1}_{k1}_{k1}_{i1}'])
        summand_list.append(summand)

    clause_list = []

    random.shuffle(summand_list)  # Shuffle the list of summands
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

    return clause_list, num_aux_vars
