from encoding import PB
import collections
import sys
import random
ALPHA = "alpha"
BETA = "beta"
GAMMA = "gamma"

class Verifier:
    def __init__(self, multiplications, m, n, p, streamlining, percentage) -> None:
        self.m = m
        self.n = n
        self.p = p
        self.multiplications = multiplications
        self.encoding_description = f"{self.m}x{self.n}_{self.n}x{self.p}_{self.multiplications}_{streamlining}_{percentage}"
        self.logs_directory = f"./opb/{self.encoding_description}"
        self.opb_encoding_file = f"{self.logs_directory}/{self.encoding_description}.opb"
        self.assignment_file = f"{self.logs_directory}/{self.encoding_description}_solver_result.txt"
        self.assignment_mapping = collections.defaultdict(int)
        self.PB = PB(self.multiplications, self.m,
                     self.n, self.p, streamlining, percentage)
        
    def create_assignment_mapping(self):
        with open(self.assignment_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("v"):
                    assignments = line[2:].split(" ")
                    for assignment in assignments:
                        variable_number = 0
                        if assignment[0] == "-":
                            variable_number = int(assignment[1:])
                            self.assignment_mapping[int(assignment[1:])] = 0
                        else:
                            variable_number = int(assignment)
                            self.assignment_mapping[int(assignment)] = 1
                        if variable_number >= self.PB.get_number_of_variables():
                            return
                        
    def get_variable_value(self, curr_variable):
        if curr_variable not in self.assignment_mapping:
            raise Exception(
                f"{curr_variable} does not exist in assignment mapping")
        return self.assignment_mapping[curr_variable]

class Verifier1(Verifier):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_compliment(self, curr_variable):
        if curr_variable == 0:
            return 1
        return 0

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
        is_negative = {1, 2, 4, 7}
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
                f"Could not satisfy ~{variables[0]} + ~{variables[1]} + ~{variables[2]} + {z_variable} >= 1")


class Verifier2(Verifier):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.multiplication_verification_file = f"{self.logs_directory}/{self.encoding_description}_verifier2.txt"
        self.verification_file = open(
            f"{self.multiplication_verification_file}", 'w+')
        self.scalar_multiplication = collections.defaultdict(dict)
        self.alpha_beta_gamma_to_var_num = self.PB.create_variables()

    def write_to_file(self, string):
        self.verification_file.write(string)

    def verify_scheme(self):
        self.create_assignment_mapping()
        self.create_scalar_multiplications_dict()
        need_to_test = 100
        schemes_tested = 0
        while schemes_tested < need_to_test:
            matrix_a, matrix_b = self.randomly_generate_matrix()
            matrix_a_flatten = [val for row in matrix_a for val in row]
            matrix_b_flatten = [val for row in matrix_b for val in row]
            naive_matrix_result = self.naive_matrix(matrix_a, matrix_b)
            brent_matrix_scheme = self.calculate_matrix(
                matrix_a_flatten, matrix_b_flatten)
            if naive_matrix_result != brent_matrix_scheme:
                raise Exception(
                    f"Error multiplying matrix {matrix_a} with {matrix_b}. Naive method results with {naive_matrix_result} and Brent equations result with {brent_matrix_scheme}. Scheme number {schemes_tested}")
            self.write_to_file(
                f"Scheme number: {schemes_tested}. Matrix A x Matrix B: {matrix_a} x {matrix_b}. Naive scheme result {naive_matrix_result}. Brent equations scheme result {brent_matrix_scheme}\n")
            schemes_tested += 1
        return True

    def randomly_generate_matrix(self):
        matrix_a = [[0 for _ in range(self.n)] for _ in range(self.m)]
        matrix_b = [[0 for _ in range(self.p)] for _ in range(self.n)]
        for i in range(self.m):
            for j in range(self.n):
                matrix_a[i][j] = random.randint(-100, 100)

        for i in range(self.n):
            for j in range(self.p):
                matrix_b[i][j] = random.randint(-100, 100)

        return matrix_a, matrix_b

    def naive_matrix(self, a_matrix_values, b_matrix_values):
        output_matrix = [[0 for _ in range(self.p)] for _ in range(self.m)]
        for i in range(self.m):
            for j in range(self.p):
                for k in range(self.n):
                    output_matrix[i][j] += a_matrix_values[i][k] * \
                        b_matrix_values[k][j]

        return [val for row in output_matrix for val in row]

    def create_scalar_multiplications_dict(self):
        for multiplication in range(self.multiplications):
            alpha_anstaz = []
            beta_anstaz = []

            for i in range(self.m):
                for j in range(self.n):
                    alpha_var = (i, j, multiplication)
                    alpha_node = self.alpha_beta_gamma_to_var_num[alpha_var][ALPHA]
                    p, q = alpha_node.first_var, alpha_node.second_var
                    alpha_anstaz.append(self.get_variable_value(
                        p) - self.get_variable_value(q))
            for i in range(self.n):
                for j in range(self.p):
                    beta_var = (i, j, multiplication)
                    beta_node = self.alpha_beta_gamma_to_var_num[beta_var][BETA]
                    r, s = beta_node.first_var, beta_node.second_var
                    beta_anstaz.append(self.get_variable_value(
                        r) - self.get_variable_value(s))

            self.scalar_multiplication[multiplication][ALPHA] = alpha_anstaz
            self.scalar_multiplication[multiplication][BETA] = beta_anstaz

    def get_M_values(self, a_matrix_values, b_matrix_values):
        m_values = [0] * self.multiplications

        for multiplication in range(self.multiplications):
            alpha_matrix_size = self.m*self.n
            alpha_anstaz_portion = self.scalar_multiplication[multiplication][ALPHA]
            beta_anstaz_portion = self.scalar_multiplication[multiplication][BETA]
            alpha_sum = beta_sum = 0

            for i in range(alpha_matrix_size):
                alpha_sum += alpha_anstaz_portion[i] * a_matrix_values[i]

            beta_matrix_size = self.n*self.p
            for i in range(beta_matrix_size):
                beta_sum += beta_anstaz_portion[i] * b_matrix_values[i]

            m_values[multiplication] = alpha_sum * beta_sum
        return m_values

    def calculate_matrix(self, a_matrix_values, b_matrix_values):
        output_matrix = []
        m_values = self.get_M_values(a_matrix_values, b_matrix_values)

        for i in range(self.m):
            for j in range(self.p):
                tot_sum = 0
                for multiplication in range(self.multiplications):
                    gamma_var = (i, j, multiplication)
                    gamma_node = self.alpha_beta_gamma_to_var_num[gamma_var][GAMMA]
                    u, v = gamma_node.first_var, gamma_node.second_var
                    tot_sum += (self.get_variable_value(
                        u) - self.get_variable_value(v)) * m_values[multiplication]
                output_matrix.append(tot_sum)

        return output_matrix

class Schemes(Verifier):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.scheme_file_name = f"{self.logs_directory}/{self.encoding_description}_scheme.txt"
        self.scheme_file = open(
            f"{self.scheme_file_name}", 'w+')
        self.scalar_multiplication = collections.defaultdict(dict)
        self.alpha_beta_gamma_to_var_num = self.PB.create_variables()

    def create_scheme(self):
        self.create_assignment_mapping()
        row_col_multiplications = {
            ALPHA: [self.m, self.n, "a"],
            BETA: [self.n, self.p, "b"],
            GAMMA: [self.m, self.p, "c"]
        }
        scheme_by_multiplication = []
        for multiplication in range(self.multiplications):
            current_multiplications = []
            for brent_var, [rows, cols, scheme_letter] in row_col_multiplications.items():
                scheme_for_var = []
                if GAMMA != brent_var:
                    for row in range(rows):
                        for col in range(cols):
                            row_col_iota_tuple = tuple((row, col, multiplication))
                            first_var = self.alpha_beta_gamma_to_var_num[row_col_iota_tuple][brent_var].first_var
                            second_var = self.alpha_beta_gamma_to_var_num[row_col_iota_tuple][brent_var].second_var
                            difference = self.get_variable_value(first_var) - self.get_variable_value(second_var)
                            row_value = row + 1 
                            col_value = col + 1 
                            sign = "-" if difference < 0 else "" 
                            if difference != 0:
                                scheme_for_var.append(sign + f"{scheme_letter}{row_value}{col_value}")
                    current_multiplications.append(scheme_for_var)
                else:
                    for col in range(cols):
                        for row in range(rows):
                            row_col_iota_tuple = tuple((row, col, multiplication))
                            first_var = self.alpha_beta_gamma_to_var_num[row_col_iota_tuple][brent_var].first_var
                            second_var = self.alpha_beta_gamma_to_var_num[row_col_iota_tuple][brent_var].second_var
                            difference = self.get_variable_value(first_var) - self.get_variable_value(second_var)
                            row_value = row + 1 
                            col_value = col + 1
                            sign = "-" if difference < 0 else "" 
                            if difference != 0:
                                scheme_for_var.append(sign + f"{scheme_letter}{col_value}{row_value}")
                    current_multiplications.append(scheme_for_var)
            scheme_by_multiplication.append(current_multiplications)
        for current_multiplication in scheme_by_multiplication:
            scheme_to_output = []
            for alpha_beta_gamma in current_multiplication:
                if not len(alpha_beta_gamma):
                    continue
                curr_var_scheme_output = ["("]
                for curr_brent_var in range(len(alpha_beta_gamma)):
                    if curr_brent_var != 0 and alpha_beta_gamma[curr_brent_var][0] != "-":
                        curr_var_scheme_output.append("+" + alpha_beta_gamma[curr_brent_var])
                    else:
                        curr_var_scheme_output.append(alpha_beta_gamma[curr_brent_var])
                curr_var_scheme_output.append(")")
                current_scheme = "".join(curr_var_scheme_output)
                scheme_to_output.append(current_scheme)
            scheme_for_curr_multiplication = "*".join(scheme_to_output)
            self.scheme_file.write(f"{scheme_for_curr_multiplication}\n")
        
if __name__ == "__main__":
    _, number_of_multiplications, m, n, p, s, c = sys.argv
    verifier = Verifier1(int(number_of_multiplications),
                        int(m), int(n), int(p), int(s), int(c))
    print("Running verifier 1!")
    if not verifier.verify_against_brent_equations():
        raise Exception("Could not verify PB encoding against Brent equations")
    print("Verifier 1 has verifier SAT assignment against the Brent equations!")
    print("Running verifier 2!")
    verifier2 = Verifier2(int(number_of_multiplications),
                          int(m), int(n), int(p), int(s), int(c))
    if not verifier2.verify_scheme():
        raise Exception("Could not verify multiplication scheme")
    print("Verifier 2 has verified scheme against naive method!")
    print("Writing scheme to file!")
    scheme = Schemes(int(number_of_multiplications),
                          int(m), int(n), int(p), int(s), int(c))
    scheme.create_scheme()
    print("Scheme was written to the file!")