from aux_list import create_aux_list
from odd import create_odd


def create_commutative_encoding_list(cumulative_dict, num_t, num_row_1, num_col_1, num_col_2):

    clause_list = []
    aux_list = create_aux_list(100000, num_t, len(cumulative_dict))
    move = 0

    for key in cumulative_dict:
        if key.startswith("t"):
            u, v, x, y, i, j = key.split("_")[2:]
            list_var = []
            list_aux = []

            if key.startswith("t_1_"):
                if v == x and y == j and u == i:
                    for m in range(1, num_t):
                        list_var.append(cumulative_dict[f't_{m}_{u}_{v}_{x}_{y}_{i}_{j}'])
                        list_aux.append(aux_list[m - 1 + move])

                    list_var.append(cumulative_dict[f't_{num_t}_{u}_{v}_{x}_{y}_{i}_{j}'])
                    odd_clauses = create_odd(list_var, list_aux)
                    move += num_t - 1

                    # Add odd constraint clauses to the clause list
                    for inner_list in odd_clauses:
                        clause_list.append(inner_list)

                else:
                    for m in range(1, num_t):
                        if m == 1:
                            list_var.append(-cumulative_dict[f't_{m}_{u}_{v}_{x}_{y}_{i}_{j}'])
                        else:
                            list_var.append(cumulative_dict[f't_{m}_{u}_{v}_{x}_{y}_{i}_{j}'])
                        list_aux.append(aux_list[m - 1 + move])

                    list_var.append(cumulative_dict[f't_{num_t}_{u}_{v}_{x}_{y}_{i}_{j}'])
                    odd_clauses = create_odd(list_var, list_aux)
                    move += num_t - 1
                    # Add odd constraint clauses to the clause list
                    for inner_list in odd_clauses:
                        clause_list.append(inner_list)

            elif key.startswith("ta_1_"):
                for m in range(1, num_t):
                    if m == 1:
                        list_var.append(-cumulative_dict[f'ta_{m}_{u}_{v}_{x}_{y}_{i}_{j}'])
                    else:
                        list_var.append(cumulative_dict[f'ta_{m}_{u}_{v}_{x}_{y}_{i}_{j}'])
                    list_aux.append(aux_list[m - 1 + move])

                list_var.append(cumulative_dict[f'ta_{num_t}_{u}_{v}_{x}_{y}_{i}_{j}'])
                odd_clauses = create_odd(list_var, list_aux)
                move += num_t - 1
                # Add odd constraint clauses to the clause list
                for inner_list in odd_clauses:
                    clause_list.append(inner_list)

            elif key.startswith("tb_1_"):
                for m in range(1, num_t):
                    if m == 1:
                        list_var.append(-cumulative_dict[f'tb_{m}_{u}_{v}_{x}_{y}_{i}_{j}'])
                    else:
                        list_var.append(cumulative_dict[f'tb_{m}_{u}_{v}_{x}_{y}_{i}_{j}'])
                    list_aux.append(aux_list[m - 1 + move])

                list_var.append(cumulative_dict[f'tb_{num_t}_{u}_{v}_{x}_{y}_{i}_{j}'])
                odd_clauses = create_odd(list_var, list_aux)
                move += num_t - 1
                # Add odd constraint clauses to the clause list
                for inner_list in odd_clauses:
                    clause_list.append(inner_list)

        elif key.startswith("s"):
            val_t, u, v, x, y = key.split("_")[1:]
            if key.startswith("s_"):
                clause_list.append([-cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                    -cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                    -cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                    -cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                    -cumulative_dict[key]])
                clause_list.append([-cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                    -cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                    cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                    cumulative_dict[key]])
                clause_list.append([-cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                    -cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                    cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                    cumulative_dict[key]])
                clause_list.append([cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                    -cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                    -cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                    cumulative_dict[key]])
                clause_list.append([cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                    cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                    -cumulative_dict[key]])
                clause_list.append([cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                    cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                    -cumulative_dict[key]])
                clause_list.append([cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                    -cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                    -cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                    cumulative_dict[key]])
                clause_list.append([cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                    cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                    -cumulative_dict[key]])
                clause_list.append([cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                    cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                    -cumulative_dict[key]])

            elif key.startswith("sa_"):
                if u != x or v != y:
                    clause_list.append([-cumulative_dict[f'aa_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])
                    clause_list.append([-cumulative_dict[f'aa_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        cumulative_dict[key]])
                    clause_list.append([-cumulative_dict[f'aa_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'aa_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'aa_{val_t}_{x}_{y}'],
                                        cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'aa_{val_t}_{x}_{y}'],
                                        cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ba_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])
                else:
                    clause_list.append([-cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'aa_{val_t}_{u}_{v}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ba_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])

            elif key.startswith("sb_"):
                if u != x or v != y:
                    clause_list.append([-cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'bb_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])
                    clause_list.append([-cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'bb_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        cumulative_dict[key]])
                    clause_list.append([-cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'bb_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                        -cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                        cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ab_{val_t}_{x}_{y}'],
                                        cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'bb_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'bb_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'bb_{val_t}_{u}_{v}'],
                                        cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])
                else:
                    clause_list.append([-cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        -cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'ab_{val_t}_{u}_{v}'],
                                        -cumulative_dict[key]])
                    clause_list.append([cumulative_dict[f'bb_{val_t}_{x}_{y}'],
                                        -cumulative_dict[key]])

    for key in cumulative_dict:
        if key.startswith("t"):
            val_t, u, v, x, y, i, j = key.split("_")[1:]

            if key.startswith("t_"):
                clause_list.append([-cumulative_dict[key], cumulative_dict[f's_{val_t}_{u}_{v}_{x}_{y}']])
                clause_list.append([-cumulative_dict[key], cumulative_dict[f'g_{val_t}_{i}_{j}']])
                clause_list.append([cumulative_dict[key], -cumulative_dict[f's_{val_t}_{u}_{v}_{x}_{y}'],
                                    -cumulative_dict[f'g_{val_t}_{i}_{j}']])

            elif key.startswith("ta_"):
                clause_list.append([-cumulative_dict[key], cumulative_dict[f'sa_{val_t}_{u}_{v}_{x}_{y}']])
                clause_list.append([-cumulative_dict[key], cumulative_dict[f'g_{val_t}_{i}_{j}']])
                clause_list.append([cumulative_dict[key], -cumulative_dict[f'sa_{val_t}_{u}_{v}_{x}_{y}'],
                                    -cumulative_dict[f'g_{val_t}_{i}_{j}']])

            elif key.startswith("tb_"):
                clause_list.append([-cumulative_dict[key], cumulative_dict[f'sb_{val_t}_{u}_{v}_{x}_{y}']])
                clause_list.append([-cumulative_dict[key], cumulative_dict[f'g_{val_t}_{i}_{j}']])
                clause_list.append([cumulative_dict[key], -cumulative_dict[f'sb_{val_t}_{u}_{v}_{x}_{y}'],
                                    -cumulative_dict[f'g_{val_t}_{i}_{j}']])

    return clause_list
