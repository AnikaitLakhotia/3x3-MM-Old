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


def encoding(num_t, num_row_1, num_col_1, num_col_2, streamlining):
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

    cumulative_dict = {}  # Initialize an empty dictionary to store cumulative variable mappings

    dict_list = [dict_t, dict_s, dict_a, dict_b, dict_g]

    # Combine variable dictionaries from dict_list into cumulative_dict
    for inner_dict in dict_list:
        for key, value in inner_dict.items():
            cumulative_dict[key] = value

    num_var = len(cumulative_dict)

    if streamlining != 0:
        # Create the cumulative list of SAT encoding clauses and the cumulative dictionary
        cumulative_list = create_encoding_list(cumulative_dict, num_t, num_row_1, num_col_1, num_col_2)
        num_var += (num_t - 1) * ((num_row_1 ** 2) * (num_col_2 ** 2) * (num_col_1 ** 2))
        num_clauses = len(cumulative_list)

    else:
        cumulative_list, num_aux_var = create_encoding_list_v2(cumulative_dict, num_row_1, num_col_1, num_col_2)
        num_var += num_aux_var
        num_clauses = len(cumulative_list)

    vectors_col_wise, vectors_row_wise = generate_var_list(num_t, num_row_1, num_col_1, num_col_2, cumulative_dict)
    lex_string = ""
    num_lex_clauses = 0

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

    if streamlining == 1:
        streamlining_var_list = generate_streamlining_v1()
        random.shuffle(streamlining_var_list)
        streamlining_var_list = streamlining_var_list[310:]

    elif streamlining == 2:
        streamlining_var_list = generate_streamlining_v2(num_t, num_row_1, num_col_1, num_col_2, 0.1)

    elif streamlining == 3:
        streamlining_var_list = generate_streamlining_v3(num_t, num_row_1, num_col_1, 0)

    else:
        streamlining_var_list = []

    num_clauses += len(streamlining_var_list) + num_lex_clauses

    encoding_string = f'p cnf {num_var} {num_clauses} \n'

    # Convert the clauses into CNF format and append them to the encoding string
    for innerlist in cumulative_list:
        clause = f'{innerlist}'
        clause = clause[1:-1]
        encoding_string = encoding_string + clause + " 0 \n"
        encoding_string = encoding_string.replace(',', '')
    encoding_string += streamline(streamlining_var_list, cumulative_dict)
    encoding_string += lex_string

    return encoding_string, cumulative_dict
