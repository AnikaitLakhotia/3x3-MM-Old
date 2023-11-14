from encoding import PB, Node
import collections
import sys
ALPHA = "alpha"
BETA = "beta"
GAMMA = "gamma"


class Verifier:
    def __init__(self, multiplications, m, n, p) -> None:
        self.m = m
        self.n = n
        self.p = p
        self.multiplications = multiplications
        encoding_description = f"{self.m}x{self.n}_{self.n}x{self.p}_{self.multiplications}"
        logs_directory = f"./opb/{encoding_description}"
        self.assignment_file = f"{logs_directory}/{encoding_description}_assignment.txt"
        self.assignment_mapping = collections.defaultdict(int)
        self.PB = PB(self.multiplications, self.m, self.n, self.p)

    def get_compliment(self, curr_variable):
        if curr_variable == 0:
            return 1
        return 0

    def get_variable_value(self, curr_variable):
        return self.assignment_mapping[curr_variable]

    def create_assignment_mapping(self):
        with open(self.assignment_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("v"):
                    assignments = line[2:].split(" ")
                    for assignment in assignments:
                        assignment = assignment.split("x")
                        if len(assignment) > 1:
                            if assignment[0] == "-":
                                self.assignment_mapping[int(assignment[1])] = 0
                            else:
                                self.assignment_mapping[int(assignment[1])] = 1
                        else:
                            raise Exception("Issue with spliting assignment")

    def verify_against_brent_equations(self):
        self.create_assignment_mapping()
        alpha_beta_gamma_to_var_num = self.PB.create_variables()
        for i in range(self.m):
            for j in range(self.n):
                for k in range(self.n):
                    for l in range(self.p):
                        for m in range(self.m):
                            for n in range(self.p):
                                total_sum_of_alpha_beta_gamma = 0
                                for iota in range(self.multiplications):
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
                                    total_sum_of_alpha_beta_gamma += self.verify_alpha_beta_gamma_constraints([p_for_alpha, q_for_alpha], [
                                        r_for_beta, s_for_beta], [u_for_gamma, v_for_gamma])
                                if total_sum_of_alpha_beta_gamma != self.PB.get_kronecker_delta_value(i, j, k, l, m, n):
                                    raise Exception(
                                        "Kronecker delta values are not satisfied")

        return True

    def verify_alpha_beta_gamma_constraints(self, alpha_variables, beta_variables, gamma_variables):
        sum_of_z_variables = 0
        is_negative = {1, 2, 4}
        aux_var_products = []
        for alpha_var in alpha_variables:
            for beta_var in beta_variables:
                for gamma_var in gamma_variables:
                    z_variable = self.PB.get_new_var()
                    self.verify_aux_variable_constraint(
                        [alpha_var, beta_var, gamma_var, z_variable])
                    aux_var_products.append(self.get_variable_value(
                        alpha_var)*self.get_variable_value(beta_var)*self.get_variable_value(gamma_var))
        for index, product in enumerate(aux_var_products):
            if index in is_negative:
                product *= -1
            sum_of_z_variables += product
        return sum_of_z_variables

    def verify_aux_variable_constraint(self, variables):
        z_variable = variables[-1]
        z_variable_value = self.get_variable_value(z_variable)
        for alpha_beta_or_gamma_variable in variables[:-1]:
            alpha_beta_or_gamma_variable_value = self.get_variable_value(
                alpha_beta_or_gamma_variable)
            if not (self.get_compliment(z_variable_value) + alpha_beta_or_gamma_variable_value >= 1):
                raise Exception(
                    f"Could not satisfy ~{z_variable} + {alpha_beta_or_gamma_variable} >= 1")

        variable_values = [self.get_variable_value(var) for var in variables]

        if not (self.get_compliment(variable_values[0]) + self.get_compliment(variable_values[1]) + self.get_compliment(variable_values[2]) + variable_values[3] >= 1):
            raise Exception(
                f"Could not satisfy ~{variable_values[0]} + ~{variable_values[1]} + ~{variable_values[2]} + {z_variable} >= 1")


if __name__ == "__main__":
    _, number_of_multiplications, m, n, p = sys.argv
    verifier = Verifier(int(number_of_multiplications), int(m), int(n), int(p))
    print("Running verifier 1!")
    if not verifier.verify_against_brent_equations():
        raise Exception("Could not verify PB encoding against Brent equations")
    print("Verifier 1 has verifier SAT assignment against the Brent equations!")
    print("Now running verifier 2!")
