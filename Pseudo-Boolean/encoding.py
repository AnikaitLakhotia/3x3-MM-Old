class PB:
    def __init__(self, multiplications) -> None:
        self.curr_variable = 0
        self.multiplications = multiplications
        self.file_name = f"3x3-{self.multiplications}.opb"
        self.opb_file = open(f"./opb/{self.file_name}", 'w+')

    def get_new_var(self):
        self.curr_variable += 1
        return self.curr_variable

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
                            t_for_gamma = self.get_new_var()
                            for n in range(3):
                                u_for_gamma = self.get_new_var()
                                self.create_pb_constraints([p_for_alpha, q_for_alpha], [
                                                           r_for_beta, s_for_beta], [t_for_gamma, u_for_gamma])
                                return

    def create_pb_constraints(self, alpha_variables, beta_variables, gamma_variables):
        a = alpha_variables
        b = beta_variables
        c = gamma_variables
        aux_variables = []
        for alpha_var in alpha_variables:
            for beta_var in beta_variables:
                for gamma_var in gamma_variables:
                    z_variable = self.get_new_var()
                    self.create_variable_constraint(
                        [alpha_var, beta_var, gamma_var, z_variable])

    def create_variable_constraint(self, variables):
        for variable in variables:
            self.opb_file.write(f"-1 x{variable} 1 x{variable} = 1\n")
        for alpha_beta_or_gamma_variable in variables[:-1]:
            self.opb_file.write(
                f"1 x{alpha_beta_or_gamma_variable} 1 x{variables[-1]} >= 1\n")
