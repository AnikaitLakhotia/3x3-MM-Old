from variables import create_var
from auxiliary_variables import create_t, create_s
from encoding_list import create_encoding_list
from encoding_list_v2 import create_encoding_list_v2
from streamline import streamline
from streamlining_v1 import generate_streamlining_v1
from streamlining_v2 import generate_streamlining_v2
from streamlining_v3 import generate_streamlining_v3
from generate_lex_clauses import generate_lex_encoding, generate_var_list
import random


def encoding(num_t, num_row_1, num_col_1, num_col_2, lex_order, streamlining, streamlining_parameter):
    """
    Generate the complete SAT encoding for the given parameters.

    Args:
        num_t (int): Number of 't's.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.
        lex_order (bool): Lexicographical Ordering Constraints are used if True.
        streamlining (int): Streamlining number.
        streamlining_parameter (int or float): The parameter associated with the streamlining.

    Returns:
        str: SAT encoding in CNF format.
        dict: A dict containing all the variables in the encoding(as keys) and their
              corresponding unique integer values.
    """
    shift = 0  # Initialize the shift value for variable indices
    dict_t = create_t(num_t, num_row_1, num_col_1, num_col_2, shift)
    shift = shift + len(dict_t)
    dict_s = create_s(num_t, num_row_1, num_col_1, num_col_2, shift)
    shift = shift + len(dict_s)
    dict_a = create_var(num_t, num_row_1, num_col_1, shift, "a")
    shift = shift + len(dict_a)
    dict_b = create_var(num_t, num_col_1, num_col_2, shift, "b")
    shift = shift + len(dict_b)
    dict_g = create_var(num_t, num_row_1, num_col_2, shift, "g")
    cumulative_dict = {}  # Initialize an empty dictionary to store cumulative variable mappings

    dict_list = [dict_t, dict_s, dict_a, dict_b, dict_g]

    # Combine variable dictionaries from dict_list into cumulative_dict
    for inner_dict in dict_list:
        for key, value in inner_dict.items():
            cumulative_dict[key] = value

    num_var = len(cumulative_dict)

    if streamlining != 0:
        # Create the cumulative list of SAT encoding clauses using main scheme.
        cumulative_list = create_encoding_list(cumulative_dict, num_t, num_row_1, num_col_1, num_col_2)
        num_var += (num_t - 1) * ((num_row_1 ** 2) * (num_col_2 ** 2) * (num_col_1 ** 2))
        num_clauses = len(cumulative_list)

    else:
        # Create the cumulative list of SAT encoding clauses using alternate scheme.
        cumulative_list, num_aux_var = create_encoding_list_v2(cumulative_dict, num_row_1, num_col_1, num_col_2)
        num_var += num_aux_var
        num_clauses = len(cumulative_list)

    lex_string = ""
    num_lex_clauses = 0

    if lex_order:
        # Generate vectors for lex ordering.
        vectors_col_wise, vectors_row_wise = generate_var_list(num_t, num_row_1, num_col_1, num_col_2, cumulative_dict)

        # Generate lex ordering clauses.
        for i in range(1, len(vectors_col_wise)):
            lex_addition, num_added_aux_var, num_added_clauses = generate_lex_encoding(vectors_col_wise[i - 1],
                                                                                       vectors_col_wise[i], num_var)
            lex_string += lex_addition
            num_var += num_added_aux_var
            num_lex_clauses += num_added_clauses
        for i in range(1, len(vectors_row_wise)):
            lex_addition, num_added_aux_var, num_added_clauses = generate_lex_encoding(vectors_row_wise[i - 1],
                                                                                       vectors_row_wise[i], num_var)
            lex_string += lex_addition
            num_var += num_added_aux_var
            num_lex_clauses += num_added_clauses

    # Add streamlining clauses.
    if streamlining == 1:
        streamlining_var_list = generate_streamlining_v1()
        random.shuffle(streamlining_var_list)
        streamlining_parameter = int(streamlining_parameter)
        streamlining_var_list = streamlining_var_list[:streamlining_parameter]
    elif streamlining == 2:
        streamlining_var_list = generate_streamlining_v2(num_t, num_row_1, num_col_1, num_col_2, streamlining_parameter)
    elif streamlining == 3:
        streamlining_var_list = generate_streamlining_v3(num_t, num_row_1, num_col_1, streamlining_parameter)
    else:
        streamlining_var_list = []

    num_clauses += len(streamlining_var_list) + num_lex_clauses

    encoding_string = f'p cnf {num_var} {num_clauses} \n'

    # Convert the clauses into CNF format, append them to
    # the encoding string and add streamlining clauses and lex string.
    encoding_string += ''.join([' '.join(map(str, innerlist)) + ' 0 \n' for innerlist in cumulative_list])
    encoding_string += streamline(streamlining_var_list, cumulative_dict)
    encoding_string += lex_string

    return encoding_string, cumulative_dict
