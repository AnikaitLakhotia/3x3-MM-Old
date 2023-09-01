def create_t(num_t, dim, shift):
    """
        Create variables representing 't's in the SAT encoding.

        Args:
            num_t (int): Number of 't' variables to create.
            dim (int): Dimensions of matrix.
            shift (int): Current variable index offset.

        Returns:
            dict: Dictionary of 't' variables and their corresponding indices.
        """

    t_dict = {}

    val_t = 't'
    val_t_range = range(1, num_t + 1)
    val_i1_range = range(1, dim + 1)
    val_i2_range = range(1, dim + 1)
    val_j1_range = range(1, dim + 1)
    val_j2_range = range(1, dim + 1)
    val_k1_range = range(1, dim + 1)
    val_k2_range = range(1, dim + 1)

    index = 1
    for t in val_t_range:
        for i1 in val_i1_range:
            for i2 in val_i2_range:
                for j1 in val_j1_range:
                    for j2 in val_j2_range:
                        for k1 in val_k1_range:
                            for k2 in val_k2_range:
                                key = f"{val_t}_{t}_{i1}_{i2}_{j1}_{j2}_{k1}_{k2}"
                                t_dict[key] = shift + index
                                index += 1
    return t_dict


def create_s(num_t, dim, shift):
    """
        Create variables representing 's'es in the SAT encoding.

        Args:
            num_t (int): Number of 's' variables to create.
            dim (int): Dimensions of matrix.
            shift (int): Current variable index offset.

        Returns:
            dict: Dictionary of 's' variables and their corresponding indices.
        """

    s_dict = {}

    val_s = 's'
    val_t_range = range(1, num_t + 1)
    val_i1_range = range(1, dim + 1)
    val_i2_range = range(1, dim + 1)
    val_j1_range = range(1, dim + 1)
    val_j2_range = range(1, dim + 1)

    index = 1
    for t in val_t_range:
        for i1 in val_i1_range:
            for i2 in val_i2_range:
                for j1 in val_j1_range:
                    for j2 in val_j2_range:
                        key = f"{val_s}_{t}_{i1}_{i2}_{j1}_{j2}"
                        s_dict[key] = shift + index
                        index += 1
    return s_dict
