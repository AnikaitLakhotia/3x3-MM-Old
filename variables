def create_var(num_t, dim, shift, var):
    """
        Create variables representing custom 'var's in the SAT encoding.

        Args:
            num_t (int): Number of custom 'var' variables to create.
            dim (int): Dimensions of matrix.
            shift (int): Current variable index offset.
            var (str): Custom variable prefix.

        Returns:
            dict: Dictionary of custom 'var' variables and their corresponding indices.
        """

    var_dict = {}

    val_s = f'{var}'
    val_t_range = range(1, num_t + 1)
    val_1_range = range(1, dim + 1)
    val_2_range = range(1, dim + 1)

    index = 1
    for t in val_t_range:
        for var_index_1 in val_1_range:
            for var_index_2 in val_2_range:
                key = f"{val_s}_{t}_{var_index_1}_{var_index_2}"
                var_dict[key] = shift + index
                index += 1
    return var_dict
