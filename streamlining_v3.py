import random


def generate_streamlining_v3(num_t, num_row_1, num_col_1, num_two_terms):
    """
    Generate a list of streamlining variables based on streamlining 3.

    Args:
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

    summand_list = []

    # Generate summands
    for val_t in val_t_range:
        summand = []
        for i1 in val_i1_range:
            for j1 in val_j1_range:
                for k1 in val_k1_range:
                    summand.append(f't_{val_t}_{i1}_{j1}_{j1}_{k1}_{k1}_{i1}')
        summand_list.append(summand)

    streamlining_list = []

    random.shuffle(summand_list)  # Shuffle the list of summands
    num_two_terms = int(num_two_terms)
    selected_summands = summand_list[:num_two_terms]  # Select the specified number of summands
    remaining_summands = summand_list[num_two_terms:]  # The remaining summands

    # Randomly sample two variables from each selected summand
    for summand in selected_summands:
        sampled_vars = random.sample(summand, 2)
        for var in sampled_vars:
            streamlining_list.append(var)

    # Randomly sample one variable from each remaining summand
    for summand in remaining_summands:
        sampled_var = random.sample(summand, 1)
        streamlining_list.append(sampled_var[0])

    return streamlining_list
