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

    sampled_indices = []  # List to store sampled indices

    for summand in selected_summands:
        valid_indices = [i for i in range(len(summand)) if i not in sampled_indices]
        sampled_indices += random.sample(valid_indices, 2)  # Sample two random indices from the remaining valid indices
        sampled_vars = [summand[i] for i in sampled_indices]
        streamlining_list.extend(sampled_vars)

    # Randomly sample one variable from each remaining summand
    for summand in remaining_summands:
        valid_indices = [i for i in range(len(summand)) if i not in sampled_indices]
        sampled_index = random.choice(valid_indices)  # Choose a random index from the remaining valid indices
        sampled_var = summand[sampled_index]
        sampled_indices.append(sampled_index)
        streamlining_list.append(sampled_var)

    type_3_vars = []
    for summand in summand_list:
        for var in summand:
            type_3_vars.append(var)

    remaining_vars = [x for x in type_3_vars if x not in streamlining_list]

    for var in remaining_vars:
        streamlining_list.append(f'-{var}')

    return streamlining_list
