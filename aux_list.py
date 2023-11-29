def create_aux_list(t, num_t, shift):
    """
    Create a list of auxiliary variables for enforcing the 'odd' constraint between
    the cubic terms (t-variables) of the respective Brent equation.

    Args:
        t (int): Number of variables of type t_a_b_c_d_e_f.
        num_t (int): Number of 't's in each Brent equation.
        shift (int): Current variable index offset.

    Returns:
        list_aux (list): List of auxiliary variables.

    Notes:
        1. Shift is used to ensure the auxiliary variables are unique, not only in their list,
           but also with respect to values for other variables in the encoding.
    """
    # Initialize count based on the shift
    count = shift + 1
    list_aux = []

    # Loop to generate auxiliary variables
    for i in range(0, t * (num_t - 1)):
        list_aux.append(count + i)

    # Return the list of auxiliary variables
    return list_aux
