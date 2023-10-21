"""
def generate_clause(X):
    clause = []
    for x in X:
        clause.append(x)
    return clause

def generate_implication_clause(X, Y):
    clause = []
    for x in X:
        clause.append(-x)
    for y in Y:
        clause.append(y)
    return clause

# Generate clauses encoding that the vector X is lexicographically less than (or equal to if strict is false) vector Y
def generate_lex_clauses(X, Y, strict, total_vars):
    clauses = []
    n = len(X)
    clauses.append(generate_implication_clause({X[0]}, {Y[0]}))
    clauses.append(generate_implication_clause({X[0]}, {total_vars+1}))
    clauses.append(generate_clause({Y[0], total_vars+1}))
    for k in range(1, n-1):
        clauses.append(generate_implication_clause({total_vars+k}, {-X[k], Y[k]}))
        clauses.append(generate_implication_clause({total_vars+k}, {-X[k], total_vars+k+1}))
        clauses.append(generate_implication_clause({total_vars+k}, {Y[k], total_vars+k+1}))
    if strict:
        clauses.append(generate_implication_clause({total_vars+n-1}, {-X[n-1]}))
        clauses.append(generate_implication_clause({total_vars+n-1}, {Y[n-1]}))
    else:
        clauses.append(generate_implication_clause({total_vars+n-1}, {-X[n-1], Y[n-1]}))
    return (clauses, total_vars+n-1)

y = [2, 3, 4]
e = [5, 6, 7]
print(generate_lex_clauses(y,e,0, 6))
"""


def generate_lex_encoding(vector_1, vector_2, num_var):
    encoding_string = ""
    num_aux_var = len(vector_1) - 1
    encoding_string += (
        f'-{vector_1[0]} {vector_2[0]} {num_var + 1} 0 \n'
        f'{vector_1[0]} -{vector_2[0]} {num_var + 1} 0 \n'
        f'{vector_1[0]} {vector_2[0]} -{num_var + 1} 0 \n'
        f'{vector_1[0]} {vector_2[0]} {num_var + 1} 0 \n'
        )

    for i in range(1, num_aux_var):
        aux_var = i + num_var
        encoding_string += (
            f'-{vector_1[i]} -{vector_2[i]} -{aux_var} {aux_var + 1} 0 \n'
            f'-{vector_1[i]} {vector_2[i]} -{aux_var + 1} 0 \n'
            f'{vector_1[i]} -{vector_2[i]} -{aux_var + 1} 0 \n'
            f'{vector_1[i]} {vector_2[i]} -{aux_var} {aux_var + 1} 0 \n'
            f'{aux_var} -{aux_var + 1} 0 \n'
        )

    for i in range(1, num_aux_var + 1):
        aux_var = i + num_var
        encoding_string += (
            f'-{vector_1[i]} {vector_2[i]} -{aux_var} 0 \n'
        )

    num_clauses = encoding_string.count(' 0 \n')
    return encoding_string, num_aux_var, num_clauses


def generate_var_list(num_t, num_row_1, num_col_1, num_col_2, cumulative_dict):
    vectors_col_wise = []
    vectors_row_wise = []
    val_t_range = range(1, num_t + 1)  # Create a range for 't' values
    val_i1_range = val_k1_range = range(1, num_row_1 + 1)  # Create ranges for 'i1' and 'k1' values
    val_i2_range = val_j1_range = range(1, num_col_1 + 1)  # Create ranges for 'i2' and 'j1' values
    val_j2_range = val_k2_range = range(1, num_col_2 + 1)  # Create ranges for 'j2' and 'k2' values
    for val_t in val_t_range:
        vector = []
        prefixes = [f'a_{val_t}', f'b_{val_t}', f'g_{val_t}']
        for var, value in cumulative_dict.items():
            if any(var.startswith(prefix) for prefix in prefixes):
                vector.append(value)
        vectors_col_wise.append(vector)

    for i1 in val_i1_range:
        for i2 in val_i2_range:
            for j1 in val_j1_range:
                for j2 in val_j2_range:
                    for k1 in val_k1_range:
                        for k2 in val_k2_range:
                            vector = []
                            for var, value in cumulative_dict.items():
                                if ((var.startswith('a_') and var.endswith(f'{i1}_{i2}')) or
                                        (var.startswith('b_') and var.endswith(f'{j1}_{j2}')) or
                                        (var.startswith('g_') and var.endswith(f'{k1}_{k2}'))):
                                    vector.append(value)
                            vectors_row_wise.append(vector)
    return vectors_col_wise, vectors_row_wise
