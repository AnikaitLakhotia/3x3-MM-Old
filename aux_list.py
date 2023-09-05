    """
        Create a list of 'aux' variables for the SAT encoding.

        Args:
            t (int): Number of variables of type t_a_b_c_d_e_f.
            num_t (int): Number of 't' variables.
            shift (int): Current variable index offset.

        Returns:
            list_aux: List of 'aux' variable indices.
        """

    count = shift + 1
    list_aux = []
    for i in range(0, t*(num_t - 1)):
        list_aux.append(count + i)
    return list_aux
