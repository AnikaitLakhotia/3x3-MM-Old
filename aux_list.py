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

    # Input validation and value checks
    for arg_name, arg_value, min_value in zip(('t', 'num_t', 'shift'), (t, num_t, shift), (1, 2, 0)):
        if not isinstance(arg_value, int):
            raise TypeError(f'The {arg_name} argument must be an integer.')

        if arg_value < min_value:
            raise ValueError(f'Invalid value for {arg_name}. It must be greater than {min_value}.')

    # Initialize count based on the shift
    count = shift + 1
    list_aux = []

    try:
        # Loop to generate auxiliary variables
        for i in range(0, t * (num_t - 1)):
            list_aux.append(count + i)
    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f"An error occurred while running create_aux_list: {e}")

    # Return the list of auxiliary variables
    return list_aux
