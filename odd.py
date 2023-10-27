def create_odd(list_var, list_aux):
    """
    Create clauses for enforcing the 'odd' constraint (using auxiliary variables from list_aux) between
    the cubic terms (t-variables) of the specific Brent equation that the values in list_var correspond to.

    Args:
        list_var (list): List of values of t-variables.
        list_aux (list): List of auxiliary variables.

    Returns:
        list: List of clauses enforcing the 'odd' constraint.

    Notes:
        1. Auxiliary variables are integers.
        2. A 'clause' is a list of integers where each integer is either the
           value of a t-variable or an auxiliary variable.
        3. The values in list_var corresponding to each t-variable will act as the respective variables in the CNF file.
    """

    clause_list = []  # Initialize an empty list to store clauses

    for index, aux in enumerate(list_aux):
        if index != 0:
            # Add clauses for 'odd' constraint using auxiliary variables
            clause_list.append([-aux, -(aux - 1), -list_var[index + 1]])
            clause_list.append([-aux, (aux - 1), list_var[index + 1]])
            clause_list.append([aux, -(aux - 1), list_var[index + 1]])
            clause_list.append([aux, (aux - 1), -list_var[index + 1]])
        else:
            # Add clauses for 'odd' constraint for the first element in the list
            clause_list.append([-aux, -list_var[index], -list_var[index + 1]])
            clause_list.append([-aux, list_var[index], list_var[index + 1]])
            clause_list.append([aux, -list_var[index], list_var[index + 1]])
            clause_list.append([aux, list_var[index], -list_var[index + 1]])

    clause_list.append([list_aux[-1]])  # Add a clause to ensure the last auxiliary variable is included

    return clause_list  # Return the list of clauses enforcing the 'odd' constraint
