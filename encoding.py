from variables import create_var
from tseitin_variables import create_t, create_s
from encoding_list import create_encoding_list


def encoding(num_t, dim):
    """
        Generate the complete SAT encoding for the given parameters.

        Args:
            num_t (int): Number of 't' variables.
            dim (int): Dimensions of matrix.

        Returns:
            str: SAT encoding in CNF format.
        """

    shift = 0
    dict_t = create_t(num_t, dim, shift)
    shift = shift + len(dict_t)
    dict_s = create_s(num_t, dim, shift)
    shift = shift + len(dict_s)
    dict_a = create_var(num_t, dim, shift, "a")
    shift = shift + len(dict_a)
    dict_b = create_var(num_t, dim, shift, "b")
    shift = shift + len(dict_b)
    dict_g = create_var(num_t, dim, shift, "g")
    cumulative_list = create_encoding_list([dict_t, dict_s, dict_a, dict_b, dict_g])
    num_y = 5
    num_var = len(dict_t) + len(dict_s) + len(dict_a) + len(dict_b) + len(dict_g) + num_y*(int(len(dict_t)/num_t))
    num_clauses = len(cumulative_list)
    encoding_string = f'p cnf {num_var} {num_clauses} \n'
    for innerlist in cumulative_list:
        clause = f'{innerlist}'
        clause = clause[1:-1]
        encoding_string = encoding_string + clause + " 0 \n"
        encoding_string = encoding_string.replace(',', '')
    return encoding_string
    
