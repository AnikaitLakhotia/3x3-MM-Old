import collections
import os
import random
import re
"""
Global variables used in self.alpha_beta_gamma_to_var_num to get the Node storing the auxiliary variables for an alpha, beta or gamma variables for a given (row, column, iota)
"""
ALPHA = "alpha"
BETA = "beta"
GAMMA = "gamma"

"""
The Node class is a data structure used to represent the auxiliary variables for a specific alpha, beta or gamma.

Consider an \alpha_{i, j}^{\itoa} = (p - q)
self.first_var (int): stores variable which represents p
self.second_var (int): stores variable which represents q
"""


class Node:
    def __init__(self, first_variable_value, second_variable_value) -> None:
        self.first_var = first_variable_value
        self.second_var = second_variable_value

    def __str__(self) -> str:
        return f"first_var {self.first_var} second_var {self.second_var}"


"""
The PB class is used to store any associated variables and methods to create the pseudo-boolean encoding representing the Brent equations for 3x3 multiplications

Class variables:
    self.curr_variable (int): a global counter variable to represent the number currently used in the encoding. It is also used to get a fresh variable for the encoding
    self.multiplications (int): represents the number of multiplications we want to try and find a multiplication scheme for
    self.file_name (string): creates an .opb file which constraints the PB encoding will be written to
    self.opb_file (File Pointer): a file pointer to the self.file_name file
    self.alpha_beta_gamma_to_var_num (dictionary: {tuple: {string: Node}}): stores a mapping from a certain (row, column, iota) to the alpha, beta and gamma variables for that given entry. The auxiliary variables (Node) for a given alpha, beta and gamma can be accessed using the global ALPHA, BETA and GAMMA variables.
"""


class PB:
    def __init__(self, multiplications, m, n, p, streamlining, percentage) -> None:
        self.curr_variable = 0
        self.m = m
        self.n = n
        self.p = p
        self.multiplications = multiplications
        self.streamlining = streamlining
        self.percentage_of_variables_changed = percentage
        encoding_description = f"{self.m}x{self.n}_{self.n}x{self.p}_{self.multiplications}_{self.streamlining}_{self.percentage_of_variables_changed}"
        logs_directory = f"./opb/{encoding_description}"
        os.makedirs(logs_directory, exist_ok=True)
        self.file_name = f"{logs_directory}/{encoding_description}.opb"
        self.opb_file = open(self.file_name, 'w')
        self.schemes_folder = "./schemes"
        self.encoding = []

    def get_new_var(self):
        """
        Returns an integer representing a new variable

        Args:
            N/A

        Returns:
            self.curr_variable: an integer which can be used to represent a variable
        """
        self.curr_variable += 1
        return self.curr_variable

    def get_kronecker_delta_value(self, i, j, k, l, m, n):
        """
        Calculates kronecker delta values based on the matrix positions for the alpha, beta and gamma

        Args:
            i (int): row for alpha
            j (int): col for alpha
            k (int): row for beta
            l (int): col for beta
            m (int): row for gamma
            n (int): col for gamma

        Returns:
            int: 1 if kronecker delta conditions are satsfied else 0
        """
        if j == k and i == m and l == n:
            return 1
        return 0

    def streamlining1(self, alpha_beta_gamma_to_var_num):
        def pick_random_file():
            if not os.path.isdir(self.schemes_folder):
                raise ValueError(
                    f"{self.schemes_folder} is not a valid directory.")

            subfolders = [f for f in os.listdir(self.schemes_folder) if os.path.isdir(
                os.path.join(self.schemes_folder, f))]

            if not subfolders:
                raise ValueError(
                    f"No subfolders found in {self.schemes_folder}.")

            random_subfolder = random.choice(subfolders)

            files_in_subfolder = [f for f in os.listdir(os.path.join(self.schemes_folder, random_subfolder)) if os.path.isfile(
                os.path.join(self.schemes_folder, random_subfolder, f))]

            if not files_in_subfolder:
                raise ValueError(
                    f"No files found in {os.path.join(self.schemes_folder, random_subfolder)}.")

            random_file = random.choice(files_in_subfolder)

            return os.path.join(self.schemes_folder, random_subfolder, random_file)

        def parse_file(file_path):
            multiplication = 0
            positive_numbers = set()
            negative_numbers = set()

            with open(file_path) as file:
                scheme_brent_variable_assignment = file.readlines()
                for assignment in scheme_brent_variable_assignment:
                    if not assignment.strip():
                        continue

                    brent_variables = assignment.split("*")

                    for brent_variable in brent_variables:
                        matches = re.findall(r'([+-]?\w+)', brent_variable)

                        for match in matches:
                            if match[0] == '-':
                                negative_numbers.add(
                                    (match[1:], multiplication))
                            else:
                                positive_numbers.add(
                                    (match.lstrip('+'), multiplication))
                    multiplication += 1

            return positive_numbers, negative_numbers

        postitive_variables, negative_variables = parse_file(
            pick_random_file())
        variable_assignments = []
        row_col_multiplications = {
            ALPHA: [self.m, self.n, "a"],
            BETA: [self.n, self.p, "b"],
            GAMMA: [self.m, self.p, "c"]
        }
        for brent_var, (rows, cols, schema_var) in row_col_multiplications.items():
            for row in range(1, rows+1):
                for col in range(1, cols+1):
                    for iota in range(self.multiplications):
                        scheme_key = (schema_var+str(row)+str(col), iota)
                        row_val = row - 1
                        col_val = col - 1
                        if brent_var == GAMMA:
                            row_val, col_val = col_val, row_val
                        if scheme_key in postitive_variables:
                            postitive_variables.remove(scheme_key)
                            variable_assignments.append(
                                (brent_var, row_val, col_val, iota, 1))
                        elif scheme_key in negative_variables:
                            negative_variables.remove(scheme_key)
                            variable_assignments.append(
                                (brent_var, row_val, col_val, iota, -1))
                        else:
                            variable_assignments.append(
                                (brent_var, row_val, col_val, iota, 0))
        random.shuffle(variable_assignments)

        percentage_of_variables = self.percentage_of_variables_changed / 100

        variable_assignments = variable_assignments[:(
            round(len(variable_assignments)*percentage_of_variables))]

        for brent_var, row_val, col_val, iota, val in variable_assignments:
            node_entry = (row_val, col_val, iota)
            brent_variable = alpha_beta_gamma_to_var_num[node_entry][brent_var]
            if val == -1:
                self.write_to_file(
                    f"1 x{brent_variable.first_var} -1 x{brent_variable.second_var} = -1;\n")
            elif val == 1:
                self.write_to_file(
                    f"1 x{brent_variable.first_var} -1 x{brent_variable.second_var} = 1;\n")
            else:
                self.write_to_file(
                    f"1 x{brent_variable.first_var} -1 x{brent_variable.second_var} = 0;\n")

    def streamlining2(self, alpha_beta_gamma_to_var_num):
        zero_variables = []
        for iota in range(self.multiplications):
            for i in range(self.m):
                for j in range(self.n):
                    for k in range(self.n):
                        for l in range(self.p):
                            for m in range(self.m):
                                for n in range(self.p):
                                    if self.get_kronecker_delta_value(i, j, k, l, m, n) == 0:
                                        alpha_coord = (i, j, iota)
                                        beta_coord = (k, l, iota)
                                        gamma_coord = (m, n, iota)
                                        alpha_variables = alpha_beta_gamma_to_var_num[alpha_coord][ALPHA]
                                        beta_variables = alpha_beta_gamma_to_var_num[beta_coord][BETA]
                                        gamma_variables = alpha_beta_gamma_to_var_num[gamma_coord][GAMMA]
                                        zero_variables.append(
                                            [alpha_variables, beta_variables, gamma_variables])

        random.shuffle(zero_variables)
        zero_variables = zero_variables[:(
            round(len(zero_variables)*self.percentage_of_variables_changed))]

        for variables in zero_variables:
            random_number = round(random.uniform(0, 2))
            variable = variables[random_number]
            self.write_to_file(
                f"1 x{variable.first_var} -1 x{variable.second_var} = 0;\n")

    def streamlining3(self, alpha_beta_gamma_to_var_num):
        for i in range(self.m):
            for j in range(self.n):
                for k in range(self.n):
                    for l in range(self.p):
                        for m in range(self.m):
                            for n in range(self.p):
                                if self.get_kronecker_delta_value(i, j, k, l, m, n):
                                    summands = []
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
                                        summands.append(
                                            [p_for_alpha, q_for_alpha, r_for_beta, s_for_beta, u_for_gamma, v_for_gamma])
                                    random.shuffle(summands)
                                    for _ in range(19):
                                        variables = summands.pop()
                                        self.write_to_file(
                                            "1 x{} -1 x{} 1 x{} -1 x{} 1 x{} -1 x{} = 1;\n".format(*variables))
                                    for _ in range(4):
                                        variables = summands.pop()
                                        self.write_to_file(
                                            "1 x{} -1 x{} 1 x{} -1 x{} 1 x{} -1 x{} = 2;\n".format(*variables))

    def write_to_file(self, constraint):
        """
        Writes a constraint to the self.opb_file file pointer.

        Args:
            constraint (string): any constraint in opb form

        Returns:
            N/A
        """
        try:
            self.opb_file.write(constraint)
            self.opb_file.flush()
        except Exception as e:
            print(f"Error writing to file: {e}")

    def create_variables(self):
        """
        Creates the auxiliary variables for all alpha, beta and gamma variables for all combinations of (row, col, iotas)

        Args:
            N/A

        Returns:
            N/A
        """
        row_col_multiplications = {
            ALPHA: [self.m, self.n],
            BETA: [self.n, self.p],
            GAMMA: [self.m, self.p]
        }
        local_alpha_beta_gamma_to_var_num = collections.defaultdict(dict)
        for brent_var, (rows, cols) in row_col_multiplications.items():
            for row in range(rows):
                for col in range(cols):
                    for iota in range(self.multiplications):
                        row_col_iota_tuple = tuple((row, col, iota))
                        first_new_var = self.get_new_var()
                        second_new_var = self.get_new_var()
                        variable_node = Node(first_new_var, second_new_var)
                        local_alpha_beta_gamma_to_var_num[row_col_iota_tuple][brent_var] = variable_node
        return local_alpha_beta_gamma_to_var_num

    def create_encoding(self):
        """
        Main function which drives the logic for creating the PB Brent equations for the encoding. It also calculates the number of variabels and constraints expected to be created by the encoding.

        Args:
            N/A

        Returns:
            N/A

        Other functions called:
            create_variables, create_alpha_beta_gamma_constraints, kronecker_delta_values
        """
        number_of_variables = self.multiplications*2*(self.m*self.n + self.n*self.p + self.m*self.p) + \
            self.m*self.n*self.n*self.p*self.m*self.p*self.multiplications*8
        number_of_constraints = self.m*self.n*self.n*self.p*self.m*self.p * \
            self.multiplications*8*4 + self.m*self.n*self.n*self.p*self.m*self.p
        self.write_to_file(
            f"* #variable= {number_of_variables} #constraint= {number_of_constraints}\n")
        # (row, column, iota) -> {alpha: Node, beta: Node, gamma: Node)
        alpha_beta_gamma_to_var_num = self.create_variables()
        for i in range(self.m):
            for j in range(self.n):
                for k in range(self.n):
                    for l in range(self.p):
                        for m in range(self.m):
                            for n in range(self.p):
                                total_alpha_beta_gamma_constraint = []
                                for iota in range(self.multiplications):
                                    # Gets auxiliary variables for alpha, beta and gamma variables
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

                                    curr_var_constraint = self.create_alpha_beta_gamma_constraints([p_for_alpha, q_for_alpha], [
                                        r_for_beta, s_for_beta], [u_for_gamma, v_for_gamma])
                                    # Gets alpha*beta*gamma constraint for a given iota
                                    total_alpha_beta_gamma_constraint.append(
                                        curr_var_constraint)
                                # Creates constraint for the summation of all alpha, beta, gamma products (long list of z) for all iotas
                                total_contraint = " ".join(
                                    clause for sub_constraint in total_alpha_beta_gamma_constraint for clause in sub_constraint)
                                self.write_to_file(
                                    f"{total_contraint} = {self.get_kronecker_delta_value(i, j, k, l, m, n)};\n")
                                # return
        if self.streamlining == 1:
            self.streamlining1(alpha_beta_gamma_to_var_num)
        elif self.streamlining == 2:
            self.streamlining2(alpha_beta_gamma_to_var_num)
        elif self.streamlining == 3:
            self.streamlining3(alpha_beta_gamma_to_var_num)

        self.opb_file.close()

    def create_alpha_beta_gamma_constraints(self, alpha_variables, beta_variables, gamma_variables):
        """
        A driver function which calls create_aux_variable_constraint to create the auxiliary variable constraints for a given alpha*beta*gamma expression. Recall, we introduce a z auxiliary variable for the multiplication of an alpha auxiliary variables times a beta auxiliary variable times a gamma auxiliary variables. For example, z = p*r*s. An auxiliary variable is introduced for all combinations of the multiplications of the alpha's, beta's and gamma's auxiliary variables (e.g. z1 = p*r*u, z2 = p*r*v, z3 = p*s*u etc...)
        Args:
            alpha_variables ([Int]): stores the two auxiliary variables for the alpha term. E.g [p, q]
            beta_variables ([Int]): stores the two auxiliary variables for the beta term. E.g [r, s]
            gamma_variables ([Int]): stores the two auxiliary variables for the gamma term. E.g [u, v]

        Returns:
            complete_aux_var_constaint ([String]): Returns a array containing the z auxiliary variables
        """
        aux_variables = []
        # Used to mark which terms should be negative
        is_negative = {1, 2, 4, 7}
        # Creates all combinations of Brent variable's auxiliary terms
        for alpha_var in alpha_variables:
            for beta_var in beta_variables:
                for gamma_var in gamma_variables:
                    z_variable = self.get_new_var()
                    self.create_aux_variable_constraint(
                        [alpha_var, beta_var, gamma_var, z_variable])
                    aux_variables.append(z_variable)
        complete_aux_var_constaint = []
        # Creates summation of the z auxiliary variables
        for aux_variable_idx, aux_variable in enumerate(aux_variables):
            if aux_variable_idx in is_negative:
                complete_aux_var_constaint.append(f"-1 x{aux_variable}")
            else:
                complete_aux_var_constaint.append(f"1 x{aux_variable}")
        return complete_aux_var_constaint

    def create_aux_variable_constraint(self, variables):
        """
        Writes the constraints for a given z's auxiliary variable for an alpha, beta, gamma multiplication.
        For example, z = p*r*v

        Args:
            variables ([int]): array stores the auxiliary variables for a given alpha, beta, gamma multiplication in the following format [variable for alpha, variable for beta, variable for gamma, z auxiliary variable]
        Returns:
            N/A
        Other functions called:
            write_to_file

        """
        # ~z + p >= 1
        for alpha_beta_or_gamma_variable in variables[:-1]:
            self.write_to_file(
                f"-1 x{variables[-1]} 1 x{alpha_beta_or_gamma_variable} >= 0;\n")

        # ~p + ~r + ~u + z >= 1
        self.write_to_file(
            "-1 x{} -1 x{} -1 x{} 1 x{} >= -2;\n".format(*variables))
        return