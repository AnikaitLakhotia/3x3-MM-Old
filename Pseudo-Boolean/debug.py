# Script used for debugging to determine error in encoding.
import collections
m_size = 3
n_size = 3
p_size = 3
multiplications = 23
ALPHA = "alpha"
BETA = "beta"
GAMMA = "gamma"
curr_variable = 0
assignment_mapping = collections.defaultdict(int)
assignmentfile = "/home/a58kapoo/research/3x3-MM/Pseudo-Boolean/opb/3x3_3x3_23_1/3x3_3x3_23_1_assignment.txt"
error_file = open("error_file.txt", "w")


def get_new_var():
    global curr_variable
    curr_variable += 1
    return curr_variable


class Node:
    def __init__(self, first_variable_value, second_variable_value) -> None:
        self.first_var = first_variable_value
        self.second_var = second_variable_value

    def __str__(self) -> str:
        return f"first_var {self.first_var} second_var {self.second_var}"


with open(assignmentfile, 'r') as file:
    for line in file:
        line = line.strip()
        if line.startswith("v"):
            assignments = line[2:].split(" ")
            for assignment in assignments:
                assignment = assignment.split("x")
                if len(assignment) > 1:
                    if assignment[0] == "-":
                        assignment_mapping[int(assignment[1])] = 0
                    else:
                        assignment_mapping[int(assignment[1])] = 1
                else:
                    raise Exception("Issue with spliting assignment")


def get_complement(var):
    if var == 1:
        return 0
    return 1


def get_kronecker_delta_value(i, j, k, l, m, n):
    if j == k and i == m and l == n:
        return 1
    return 0

# pru - prv ...


def create_alpha_beta_gamma_constraints(alpha_variables, beta_variables, gamma_variables):
    aux_variables = []
    is_negative = {1, 2, 4, 7}
    for alpha_var in alpha_variables:
        for beta_var in beta_variables:
            for gamma_var in gamma_variables:
                z_variable = get_new_var()
                assignment_mapping[z_variable] = assignment_mapping[alpha_var] * \
                    assignment_mapping[beta_var]*assignment_mapping[gamma_var]
                create_aux_variable_constraint(
                    [alpha_var, beta_var, gamma_var, z_variable])
                aux_variables.append(z_variable)
    complete_aux_var_constaint = []
    for aux_variable_idx, aux_variable in enumerate(aux_variables):
        if aux_variable_idx in is_negative:
            complete_aux_var_constaint.append([aux_variable, -1])
        else:
            complete_aux_var_constaint.append([aux_variable, 1])
    return complete_aux_var_constaint


def create_aux_variable_constraint(variables):
    global alpha_beta_or_gamma_variable_value
    z_var_value = assignment_mapping[variables[-1]]
    for alpha_beta_or_gamma_variable in variables[:-1]:
        alpha_beta_or_gamma_variable_value = assignment_mapping[
            alpha_beta_or_gamma_variable]
        if not (get_complement(z_var_value) + alpha_beta_or_gamma_variable_value) >= 1:
            raise Exception(
                f"{variables[-1]} + {alpha_beta_gamma_to_var_num} >= 1 is not satisfied")

    if not (get_complement(assignment_mapping[variables[0]]) + get_complement(assignment_mapping[variables[1]]) + get_complement(assignment_mapping[variables[2]]) + assignment_mapping[variables[-1]] >= 1):
        raise Exception(
            f"Could not satisfy ~{variables[0]} + ~{variables[1]} + ~{variables[2]} + {variables[-1]} >= 1")


row_col_multiplications = {
    ALPHA: [m_size, n_size],
    BETA: [n_size, p_size],
    GAMMA: [m_size, p_size]
}
alpha_beta_gamma_to_var_num = collections.defaultdict(dict)
for brent_var, (rows, cols) in row_col_multiplications.items():
    for row in range(rows):
        for col in range(cols):
            for iota in range(multiplications):
                row_col_iota_tuple = tuple((row, col, iota))
                first_new_var = get_new_var()
                second_new_var = get_new_var()
                variable_node = Node(first_new_var, second_new_var)
                alpha_beta_gamma_to_var_num[row_col_iota_tuple][brent_var] = variable_node
for i in range(m_size):
    for j in range(n_size):
        for k in range(n_size):
            for l in range(p_size):
                for m in range(m_size):
                    for n in range(p_size):
                        total_alpha_beta_gamma_constraint = []
                        for iota in range(multiplications):
                            alpha_coord = (i, j, iota)
                            beta_coord = (k, l, iota)
                            gamma_coord = (m, n, iota)
                            p_for_alpha = alpha_beta_gamma_to_var_num[
                                alpha_coord][ALPHA].first_var
                            q_for_alpha = alpha_beta_gamma_to_var_num[
                                alpha_coord][ALPHA].second_var
                            r_for_beta = alpha_beta_gamma_to_var_num[beta_coord][BETA].first_var
                            s_for_beta = alpha_beta_gamma_to_var_num[beta_coord][BETA].second_var
                            u_for_gamma = alpha_beta_gamma_to_var_num[
                                gamma_coord][GAMMA].first_var
                            v_for_gamma = alpha_beta_gamma_to_var_num[
                                gamma_coord][GAMMA].second_var
                            curr_var_constraint = create_alpha_beta_gamma_constraints([p_for_alpha, q_for_alpha], [
                                r_for_beta, s_for_beta], [u_for_gamma, v_for_gamma])
                            total_alpha_beta_gamma_constraint.append(
                                curr_var_constraint)
                            # stores all the z values for a given alpha*beta*gamma multiplicaiotn
                        total_contraint = [
                            clause for sub_constraint in total_alpha_beta_gamma_constraint for clause in sub_constraint]
                        tot_sum = 0
                        for var, sign in total_contraint:
                            tot_sum += (assignment_mapping[var] * sign)
                        for constraint in total_alpha_beta_gamma_constraint:
                            curr_sum = 0
                            for var, sign in constraint:
                                curr_sum += (assignment_mapping[var]*sign)
                            tot_sum += curr_sum

                        if tot_sum != get_kronecker_delta_value(i, j, k, l, m, n):
                            error_file.write(
                                f"Kronecker delta: {get_kronecker_delta_value(i, j, k, l, m, n)} is not satisfied at alpha {i} {j}  beta {k} {l} and gamma {m} {n}\n")
print("No errors")
