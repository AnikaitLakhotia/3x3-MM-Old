from variables import create_var
from auxiliary_variables import create_t, create_s
from encoding_list import create_encoding_list


def encoding(num_t, num_row_1, num_col_1, num_col_2):
    """
    Generate the complete SAT encoding for the given parameters.

    Args:
        num_t (int): Number of 't's.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.

    Returns:
        str: SAT encoding in CNF format.
    """

    shift = 0  # Initialize the shift value for variable indices
    dict_t = create_t(num_t, num_row_1, num_col_1, num_col_2, shift)
    shift = shift + len(dict_t)  # Update shift for the next set of variables
    dict_s = create_s(num_t, num_row_1, num_col_1, num_col_2, shift)
    shift = shift + len(dict_s)
    dict_a = create_var(num_t, num_row_1, num_col_1, shift, "a")
    shift = shift + len(dict_a)
    dict_b = create_var(num_t, num_col_1, num_col_2, shift, "b")
    shift = shift + len(dict_b)
    dict_g = create_var(num_t, num_row_1, num_col_2, shift, "g")

    # Create the cumulative list of SAT encoding clauses and the cumulative dictionary
    cumulative_list, cumulative_dict = create_encoding_list([dict_t, dict_s, dict_a, dict_b, dict_g],
                                                            num_t, num_row_1, num_col_1, num_col_2)

    num_var = (len(dict_t) + len(dict_s) + len(dict_a) + len(dict_b) + len(dict_g) +
               (num_t - 1) * ((num_row_1**2) * (num_col_2**2) * (num_col_1**2)))
    num_clauses = len(cumulative_list)

    encoding_string = f'p cnf {num_var} {num_clauses} \n'

    # Convert the clauses into CNF format and append them to the encoding string
    for innerlist in cumulative_list:
        clause = f'{innerlist}'
        clause = clause[1:-1]
        encoding_string = encoding_string + clause + " 0 \n"
        encoding_string = encoding_string.replace(',', '')

    return encoding_string, cumulative_dict
