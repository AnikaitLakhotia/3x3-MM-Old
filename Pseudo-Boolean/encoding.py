class PB:
    def __init__(self, multiplications) -> None:
        self.curr_variable = 0
        self.multiplications = multiplications
        self.file_name = f"3x3-{self.multiplications}.opb"
        self.opb_file = open(f"./opb/{self.file_name}", 'w+')

    def get_new_var(self):
        self.curr_variable += 1
        return self.curr_variable

    def kronecker_delta_values(self, i, j, k, l, m, n):
        if j == k and i == m and l == n:
            return 1
        return 0

    def create_encoding(self):
        for i in range(3):
            p_for_alpha = self.get_new_var()
            for j in range(3):
                q_for_alpha = self.get_new_var()
                for k in range(3):
                    r_for_beta = self.get_new_var()
                    for l in range(3):
                        s_for_beta = self.get_new_var()
                        for m in range(3):
                            u_for_gamma = self.get_new_var()
                            for n in range(3):
                                v_for_gamma = self.get_new_var()
                                total_alpha_beta_gamma_constraint = []
                                for _ in range(self.multiplications):
                                    curr_var_constraint = self.create_pb_constraints([p_for_alpha, q_for_alpha], [
                                                                                     r_for_beta, s_for_beta], [u_for_gamma, v_for_gamma])
                                    total_alpha_beta_gamma_constraint.append(
                                        curr_var_constraint)
                                total_contraint = " ".join(
                                    clause for sub_constaint in total_alpha_beta_gamma_constraint for clause in sub_constaint)
                                self.opb_file.write(
                                    f"{total_contraint} = {self.kronecker_delta_values(i, j, k, l, m, n)}\n")
                                # print(total_contraint)
                                # return

    def create_pb_constraints(self, alpha_variables, beta_variables, gamma_variables):
        aux_variables = []
        is_negative = {1, 2, 4}
        for alpha_var in alpha_variables:
            for beta_var in beta_variables:
                for gamma_var in gamma_variables:
                    z_variable = self.get_new_var()
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
        # p + ~p = 1
        for variable in variables:
            self.opb_file.write(f"-1 x{variable} 1 x{variable} = 1\n")
        # ~z + p >= 1
        for alpha_beta_or_gamma_variable in variables[:-1]:
            self.opb_file.write(
                f"-1 x{variables[-1]} 1 x{alpha_beta_or_gamma_variable} >= 1\n")

        # ~p + ~r + ~u + z >= 1
        self.opb_file.write(
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
"""
# (8*8*23 + 1)(3**6)
# 729
# 1073817
