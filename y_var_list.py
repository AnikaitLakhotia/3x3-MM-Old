def create_y_var_list(num_y, num_t, shift):
    """
        Create a list of 'y' variables for the SAT encoding.

        Args:
            num_y (int): Number of 'y' variables to create.
            num_t (int): Number of 't' variables.
            shift (int): Current variable index offset.

        Returns:
            list_y: List of 'y' variable indices.
        """

    count = shift + 1
    list_y = []
    for i in range(0, num_y*num_t + 1):
        list_y.append(count + i)
    return list_y
