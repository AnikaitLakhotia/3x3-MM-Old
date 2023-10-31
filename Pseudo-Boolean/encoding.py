import collections
ALPHA = "alpha"
BETA = "beta"
GAMMA = "gamma"


class Node:
    def __init__(self, first_variable_value, second_variable_value) -> None:
        self.first_var = first_variable_value
        self.second_var = second_variable_value

    def __str__(self) -> str:
        return f"first_var {self.first_var} second_var {self.second_var}"


class PB:
    def __init__(self, multiplications) -> None:
        self.curr_variable = 0
        self.multiplications = multiplications
        self.file_name = f"3x3-{self.multiplications}.opb"
        self.opb_file = open(f"./opb/{self.file_name}", 'w+')
        # (row, column, iota) -> {alpha: Node, beta: Node, gamma: Node)
        self.alpha_beta_gamma_to_var_num = collections.defaultdict(dict)

    def get_new_var(self):
        self.curr_variable += 1
        return self.curr_variable

    def kronecker_delta_values(self, i, j, k, l, m, n):
        if j == k and i == m and l == n:
            return 1
        return 0

    def write_to_file(self, constraint):
        self.opb_file.write(constraint)

    def create_variables(self):
        for row in range(3):
            for col in range(3):
                for iota in range(self.multiplications):
                    row_col_iota_tuple = tuple((row, col, iota))
                    for brent_var in [ALPHA, BETA, GAMMA]:
                        first_new_var = self.get_new_var()
                        second_new_var = self.get_new_var()
                        self.alpha_beta_gamma_to_var_num[row_col_iota_tuple][brent_var] = Node(
                            first_new_var, second_new_var)
                        self.write_to_file(
                            f"-1 x{first_new_var} 1 x{first_new_var} = 1\n")
                        self.write_to_file(
                            f"-1 x{second_new_var} 1 x{second_new_var} = 1\n")

    def create_encoding(self):
        self.create_variables()
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        for m in range(3):
                            for n in range(3):
                                total_alpha_beta_gamma_constraint = []
                                for iota in range(self.multiplications):
                                    alpha_coord = (i, j, iota)
                                    beta_coord = (k, l, iota)
                                    gamma_coord = (m, n, iota)
                                    p_for_alpha = self.alpha_beta_gamma_to_var_num[
                                        alpha_coord][ALPHA].first_var
                                    q_for_alpha = self.alpha_beta_gamma_to_var_num[
                                        alpha_coord][ALPHA].second_var
                                    r_for_beta = self.alpha_beta_gamma_to_var_num[beta_coord][BETA].first_var
                                    s_for_beta = self.alpha_beta_gamma_to_var_num[beta_coord][BETA].second_var
                                    u_for_gamma = self.alpha_beta_gamma_to_var_num[
                                        gamma_coord][GAMMA].first_var
                                    v_for_gamma = self.alpha_beta_gamma_to_var_num[
                                        gamma_coord][GAMMA].second_var
                                    curr_var_constraint = self.create_pb_constraints([p_for_alpha, q_for_alpha], [
                                                                                     r_for_beta, s_for_beta], [u_for_gamma, v_for_gamma])
                                    total_alpha_beta_gamma_constraint.append(
                                        curr_var_constraint)
                                total_contraint = " ".join(
                                    clause for sub_constaint in total_alpha_beta_gamma_constraint for clause in sub_constaint)
                                self.opb_file.write(
                                    f"{total_contraint} = {self.kronecker_delta_values(i, j, k, l, m, n)}\n")

    def create_pb_constraints(self, alpha_variables, beta_variables, gamma_variables):
        aux_variables = []
        is_negative = {1, 2, 4}
        for alpha_var in alpha_variables:
            for beta_var in beta_variables:
                for gamma_var in gamma_variables:
                    z_variable = self.get_new_var()
                    self.opb_file.write(
                        f"-1 x{z_variable} 1 x{z_variable} = 1\n")
                    self.create_aux_variable_constraint(
                        [alpha_var, beta_var, gamma_var, z_variable])
                    aux_variables.append(z_variable)
        complete_aux_var_constaint = []
        for aux_variable_idx, aux_variable in enumerate(aux_variables):
            if aux_variable_idx in is_negative:
                complete_aux_var_constaint.append(f"-1 x{aux_variable}")
            else:
                complete_aux_var_constaint.append(f"1 x{aux_variable}")
        return complete_aux_var_constaint

    def create_aux_variable_constraint(self, variables):
        # ~z + p >= 1
        for alpha_beta_or_gamma_variable in variables[:-1]:
            self.write_to_file(
                f"-1 x{variables[-1]} 1 x{alpha_beta_or_gamma_variable} >= 1\n")

        # ~p + ~r + ~u + z >= 1
        self.write_to_file(
            "-1 x{} -1 x{} -1 x{} 1 x{} >= 1 \n".format(*variables))


"""
alpha*beta*gamma = eight zs
    
alpha*beta*gamma = eight zs suppose kronker deltas = 0
now we have a summation of 

iota = 1

assume for this i,j,k,l,m,n kronker deltas = 0 (it does not satify)
                    iota = 1
(z1 - z2 -z3 + z4 - z5 + z6 + z7 + z8) + z9 - z10 ... z_184 = 0
8 represent the number of aux variables for some a*b*y multiplication
23 represents the number of multiplications (iota)



for an alpha beta gamma:
    6 pqrsuv, and 8 z so
    6 p + p`
    for each z, 4 eqs => 8*4 = 32
    1 summation
    thus, ((6 + 8 + 32)*2 + 1)*729 = 47

"""
# (8*8*23 + 1)(3**6)
# 729
# 1 073 817
