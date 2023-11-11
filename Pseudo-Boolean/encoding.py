import collections
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
    def __init__(self, multiplications) -> None:
        self.curr_variable = 0
        self.multiplications = multiplications
        self.file_name = f"3x3-{self.multiplications}.opb"
        self.opb_file = open(f"./opb/{self.file_name}", 'w+')
        # (row, column, iota) -> {alpha: Node, beta: Node, gamma: Node)
        self.alpha_beta_gamma_to_var_num = collections.defaultdict(dict)

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

    def write_to_file(self, constraint):
        """
        Writes a constraint to the self.opb_file file pointer.
        
        Args:
            constraint (string): any constraint in opb form
        
        Returns:
            N/A
        """
        self.opb_file.write(constraint)

    def create_variables(self):
        """
        Creates the auxiliary variables for all alpha, beta and gamma variables for all combinations of (row, col, iotas)

        Args:
            N/A
        
        Returns:
            N/A
        """
        # number of variables: 3*3*3*multiplications*2
        for row in range(3):
            for col in range(3):
                for iota in range(self.multiplications):
                    row_col_iota_tuple = tuple((row, col, iota))
                    for brent_var in [ALPHA, BETA, GAMMA]:
                        first_new_var = self.get_new_var()
                        second_new_var = self.get_new_var()
                        self.alpha_beta_gamma_to_var_num[row_col_iota_tuple][brent_var] = Node(
                            first_new_var, second_new_var)

    def create_encoding(self):
        """
        Main function which drives the logic for creating the PB Brent equations for the encoding. It also calculates the number of variabels and constraints expected to be created by the encoding.

        Args:
            N/A

        Returns:
            N/A
        
        Other functions called:
            create_variables, create_pb_constraints, kronecker_delta_values
        """
        number_of_variables = 3*3*3*self.multiplications * \
            2 + 3*3*3*3*3*3*self.multiplications*8
        number_of_constraints = 3*3*3*3*3*3 + 3 * \
            3*3*3*3*3*self.multiplications*8*4

        self.write_to_file(
            f"* #variable= {number_of_variables} #constraint= {number_of_constraints}\n")
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
                                    clause for sub_constraint in total_alpha_beta_gamma_constraint for clause in sub_constraint)
                                self.opb_file.write(
                                    f"{total_contraint} = {self.get_kronecker_delta_value(i, j, k, l, m, n)};\n")

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
                f"1 ~x{variables[-1]} 1 x{alpha_beta_or_gamma_variable} >= 1;\n")

        # ~p + ~r + ~u + z >= 1
        self.write_to_file(
            "1 ~x{} 1 ~x{} 1 ~x{} 1 x{} >= 1;\n".format(*variables))
