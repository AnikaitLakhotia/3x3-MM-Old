import random


def generate_streamlining_v3(num_t, num_row_1, num_col_1, num_two_terms):

    val_t_range = range(1, num_t + 1)  # Create a range for 't' values
    val_i1_range = val_k1_range = range(1, num_row_1 + 1)  # Create ranges for 'i1' and 'k1' values
    val_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j1' values

    summand_list = []

    for val_t in val_t_range:
        summand = []
        for i1 in val_i1_range:
            for j1 in val_j1_range:
                for k1 in val_k1_range:
                    summand.append(f't_{val_t}_{i1}_{j1}_{j1}_{k1}_{k1}_{i1}')
        summand_list.append(summand)

    streamlining_list = []

    random.shuffle(summand_list)
    selected_summands = summand_list[:num_two_terms]
    remaining_summands = summand_list[num_two_terms:]

    for summand in selected_summands:
        sampled_vars = random.sample(summand, 2)
        for var in sampled_vars:
            streamlining_list.append(var)

    for summand in remaining_summands:
        sampled_var = random.sample(summand, 1)
        streamlining_list.append(sampled_var[0])

    return streamlining_list
