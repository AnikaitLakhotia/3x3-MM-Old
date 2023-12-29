import random


def generate_streamlining_v2(num_t, num_row_1, num_col_1, num_col_2, zero_prob, commutative, seed):
    """
    Generate a list of streamlining variables based on streamlining 2.

    Args:
        num_t (int): Number of 't' values.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.
        zero_prob (float): Probability of a variable being zero.
        commutative (bool): Commutative encoding is used if True and non-commutative if False.
        seed (None or int): Seed for random() function.

    Returns:
        list: List of streamlining variables.

    This function generates a list of streamlining variables and then applies a modification by removing variables based
    on the provided probability 'zero_prob'.
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

            # Input validation for zero_prob argument
            elif not isinstance(zero_prob, float):
                raise TypeError('The zero_prob argument must be a float.')

            # Value check for zero_prob argument
            elif zero_prob < 0 or zero_prob > 1:
                raise ValueError('The zero_prob argument must be less than or equal to 1 '
                                 'and greater than or equal to 0.')
        # Input validation and value check for seed
        if seed is not None:
            try:
                int(seed)
            except ValueError:
                # Raise an exception if the conversion fails
                raise ValueError(f'Invalid value for seed. It must be None or an integer.')

        val_t_range = range(1, num_t + 1)  # Create a range for 't' values
        val_i1_range = val_k1_range = range(1, num_row_1 + 1)  # Create ranges for 'i1' and 'k1' values
        val_i2_range = val_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j1' values
        val_j2_range = val_k2_range = range(1, num_col_2 + 1)  # Create ranges for 'j2' and 'k2' values

        streamlining_list = []

        # Generate streamlining variables
        for val_t in val_t_range:
            for i1 in val_i1_range:
                for i2 in val_i2_range:
                    for j1 in val_j1_range:
                        for j2 in val_j2_range:
                            for k1 in val_k1_range:
                                for k2 in val_k2_range:
                                    if i2 == j1 or j2 == k2 or k1 == i1:
                                        streamlining_list.append(f'-t_{val_t}_{i1}_{i2}_{j1}_{j2}_{k1}_{k2}')
        if commutative:
            vala_i1_range = vala_j1_range = vala_k1_range = range(1, num_row_1 + 1)  # Create ranges for
            # 'i1', 'j1', and 'k1' values
            vala_i2_range = vala_j2_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j2' values
            vala_k2_range = range(1, num_col_2 + 1)  # Create ranges for 'k2' values

            # Generate streamlining variables
            for val_t in val_t_range:
                for i1 in vala_i1_range:
                    for i2 in vala_i2_range:
                        for j1 in vala_j1_range:
                            for j2 in vala_j2_range:
                                for k1 in vala_k1_range:
                                    for k2 in vala_k2_range:
                                        if i2 == j1 or j2 == k2 or k1 == i1:
                                            streamlining_list.append(f'-ta_{val_t}_{i1}_{i2}_{j1}_{j2}_{k1}_{k2}')

            valb_i1_range = valb_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'i1' and 'j1' values
            valb_i2_range = valb_j2_range = valb_k2_range = range(1, num_col_2 + 1)  # Create ranges for
            # 'i2', 'j2', and 'k2' values
            valb_k1_range = range(1, num_row_1 + 1)  # Create ranges for 'k1' values

            for val_t in val_t_range:
                for i1 in valb_i1_range:
                    for i2 in valb_i2_range:
                        for j1 in valb_j1_range:
                            for j2 in valb_j2_range:
                                for k1 in valb_k1_range:
                                    for k2 in valb_k2_range:
                                        if i2 == j1 or j2 == k2 or k1 == i1:
                                            streamlining_list.append(f'-tb_{val_t}_{i1}_{i2}_{j1}_{j2}_{k1}_{k2}')

        random.seed(seed)
        random.shuffle(streamlining_list)  # Shuffle the list of streamlining variables
        modified_list = streamlining_list.copy()  # Create a copy of the shuffled list

        # Set seed for random() function
        y_seed = seed
        # Modify the list based on the zero probability
        for variable in streamlining_list:
            # Set seed for random() function
            random.seed(y_seed)
            y = random.random()

            # Change seed deterministically if it's not None
            if seed is not None:
                y_seed += 1
            else:
                y_seed = None

            if y > zero_prob:
                modified_list.remove(variable)

        # Revert back to None(default) seed
        random.seed(None)

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f'An error occurred while running generate_streamlining_v2: {e}')
    return modified_list
