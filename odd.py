def create_odd(list_var, list_aux, n):
    assert len(list_var) == n, "Length of list_var not equal to n."
    assert len(list_aux) == n - 1, "Length of list_aux not equal to n - 1."
    clause_list = []
    for index, aux in enumerate(list_aux):
        if index != 0:
            clause_list.append([-aux, -(aux - 1), -list_var[index + 1]])
            clause_list.append([-aux, (aux - 1), list_var[index + 1]])
            clause_list.append([aux, -(aux - 1), list_var[index + 1]])
            clause_list.append([aux, (aux - 1), -list_var[index + 1]])
        else:
            clause_list.append([-aux, -list_var[index], -list_var[index + 1]])
            clause_list.append([-aux, list_var[index], list_var[index + 1]])
            clause_list.append([aux, -list_var[index], list_var[index + 1]])
            clause_list.append([aux, list_var[index], -list_var[index + 1]])
    clause_list.append([list_aux[-1]])
    return clause_list
