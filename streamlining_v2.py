import random

def generate_streamlining_v2(num_t, num_row_1, num_col_1, num_col_2, zero_prob):
    val_t_range = range(1, num_t + 1)  # Create a range for 't' values
    val_i1_range = val_k1_range = range(1, num_row_1 + 1)  # Create ranges for 'i1' and 'k1' values
    val_i2_range = val_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j1' values
    val_j2_range = val_k2_range = range(1, num_col_2 + 1)  # Create ranges for 'j2' and 'k2' values

    streamlining_list = []
    for val_t in val_t_range:
        for i1 in val_i1_range:
            for i2 in val_i2_range:
                for j1 in val_j1_range:
                    for j2 in val_j2_range:
                        for k1 in val_k1_range:
                            for k2 in val_k2_range:
                                if i2 != j1 and j2 != k1 and k2 != i1:
                                    streamlining_list.append(f'-t_{val_t}_{i1}_{i2}_{j1}_{j2}_{k1}_{k2}')

    random.shuffle(streamlining_list)
    modified_list = streamlining_list.copy()

    for variable in streamlining_list:
        if random.random() > zero_prob:
            modified_list.remove(variable)

    return modified_list
