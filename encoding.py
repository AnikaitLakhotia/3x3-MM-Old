from variables import create_var
from auxiliary_variables import create_t, create_s
from encoding_list import create_encoding_list
from encoding_list_v2 import create_encoding_list_v2
from commutative_encoding_list import create_commutative_encoding_list
from streamline import streamline
from streamlining_v1 import generate_streamlining_v1
from streamlining_v2 import generate_streamlining_v2
from streamlining_v3 import generate_streamlining_v3
from generate_lex_clauses import generate_lex_encoding, generate_var_list
import random


def encoding(num_t, num_row_1, num_col_1, num_col_2, commutative, lex_order,
             streamlining_0, streamlining_1, streamlining_parameter_1, streamlining_2,
             streamlining_parameter_2, streamlining_3, streamlining_parameter_3):
    """
    Generate the complete SAT encoding for the given parameters.

    Args:
        num_t (int): Number of 't's.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.
        commutative (bool): Commutative encoding is used if True and non-commutative if False.
        lex_order (bool): Lexicographical Ordering Constraints are used if True.
        streamlining_0 (bool): Streamlining 0 is used if True.
        streamlining_1 (bool): Streamlining 1 is used if True.
        streamlining_parameter_1 (int): The parameter associated with the streamlining 1.
        streamlining_2 (bool): Streamlining 2 is used if True.
        streamlining_parameter_2 (float): The parameter associated with the streamlining 2.
        streamlining_3 (bool): Streamlining 3 is used if True.
        streamlining_parameter_3 (int): The parameter associated with the streamlining 3.

    Returns:
        str: SAT encoding in CNF format.
        dict: A dict containing all the variables in the encoding(as keys) and their
              corresponding unique integer values.
    """

    try:
        # Input validation and value checks for integer arguments
        for arg_name, arg_value, min_value in zip(('num_t', 'num_row_1', 'num_col_1', 'num_col_2'),
                                                  (num_t, num_row_1, num_col_1, num_col_2),
                                                  (2, 1, 1, 1)):
            if not isinstance(arg_value, int):
                raise TypeError(f'The {arg_name} argument must be an integer.')

            elif arg_value < min_value:
                raise ValueError(f'Invalid value for {arg_name}. It must be greater than or equal to {min_value}.')

        # Input validation for boolean arguments
        for arg_name, arg_value in zip(('commutative', 'lex_order', 'streamlining_0', 'streamlining_1',
                                        'streamlining_2', 'streamlining_3'),
                                       (commutative, lex_order, streamlining_0, streamlining_1,
                                        streamlining_2, streamlining_3)):
            if not isinstance(arg_value, bool):
                raise TypeError(f'The {arg_name} argument must be a bool.')

        # Input validation and value checks for integer arguments
        for arg_name, arg_value in zip(('streamlining_parameter_1', 'streamlining_parameter_3'),
                                       (streamlining_parameter_1, streamlining_parameter_3)):
            if not isinstance(arg_value, int):
                raise TypeError(f'The {arg_name} argument must be an int.')

            # Value checks for streamlining_parameter_1
            elif (streamlining_3 and arg_name == 'streamlining_parameter_1' and
                    (arg_value > (num_t * num_row_1 * num_col_2 - 1) or arg_value < -num_t * num_row_1 * num_col_2)):
                raise ValueError(f'Invalid value for {arg_name}. It must be greater than or equal to '
                                 f'{-num_t * num_row_1 * num_col_2} and less than or equal to '
                                 f'{num_t * num_row_1 * num_col_2 - 1}')

            # Value checks for streamlining_parameter_3
            elif arg_name == 'streamlining_parameter_3' and streamlining_3 and arg_value + num_t != num_row_1 * num_col_1 * num_col_2:
                raise ValueError(f'Invalid value for {arg_name}. {arg_name} + {num_t} must be equal to '
                                 f'{num_row_1 * num_col_1 * num_col_2}')

        # Input validation for float argument
        if not isinstance(streamlining_parameter_2, float):
            raise TypeError('The streamlining_parameter_2 argument must be a float.')

        # Value check for streamlining_parameter_2
        elif streamlining_2 and (streamlining_parameter_2 < 0 or streamlining_parameter_2 > 1):
            raise ValueError('The streamlining_parameter_2 argument must be less than or equal to 1 '
                             'and greater than or equal to 0.')

        shift = 0  # Initialize the shift value for variable indices
        dict_t = create_t(num_t, num_row_1, num_col_1, num_col_2, shift, "t")
        shift = shift + len(dict_t)
        dict_s = create_s(num_t, num_row_1, num_col_1, num_col_2, shift, "s")
        shift = shift + len(dict_s)
        dict_g = create_var(num_t, num_row_1, num_col_2, shift, "g")
        cumulative_dict = {}  # Initialize an empty dictionary to store cumulative variable mappings

        if not commutative:
            shift = shift + len(dict_g)
            dict_a = create_var(num_t, num_row_1, num_col_1, shift, "a")
            shift = shift + len(dict_a)
            dict_b = create_var(num_t, num_col_1, num_col_2, shift, "b")

            dict_list = [dict_t, dict_s, dict_g, dict_a, dict_b]

            # Combine variable dictionaries from dict_list into cumulative_dict
            for inner_dict in dict_list:
                for key, value in inner_dict.items():
                    cumulative_dict[key] = value

            num_var = len(cumulative_dict)

            if not streamlining_0:
                # Create the cumulative list of SAT encoding clauses using main scheme.
                cumulative_list = create_encoding_list(cumulative_dict, num_t, num_row_1, num_col_1, num_col_2)
                num_var += (num_t - 1) * ((num_row_1 ** 2) * (num_col_2 ** 2) * (num_col_1 ** 2))

            else:
                # Create the cumulative list of SAT encoding clauses using alternate scheme.
                cumulative_list, num_aux_var = create_encoding_list_v2(cumulative_dict, num_t, num_row_1,
                                                                       num_col_1, num_col_2)
                num_var += num_aux_var

        else:
            shift = shift + len(dict_g)
            dict_aa = create_var(num_t, num_row_1, num_col_1, shift, "aa")
            shift = shift + len(dict_aa)
            dict_bb = create_var(num_t, num_col_1, num_col_2, shift, "bb")
            shift = shift + len(dict_bb)
            dict_ab = create_var(num_t, num_col_1, num_col_2, shift, "ab")
            shift = shift + len(dict_ab)
            dict_ba = create_var(num_t, num_row_1, num_col_1, shift, "ba")
            shift = shift + len(dict_ba)
            dict_sa = create_s(num_t, num_row_1, num_col_1, num_col_2, shift, "sa")
            shift = shift + len(dict_sa)
            dict_sb = create_s(num_t, num_col_1, num_col_2, num_col_2, shift, "sb")
            shift = shift + len(dict_sb)
            dict_ta = create_t(num_t, num_row_1, num_col_1, num_col_2, shift, "ta")
            shift = shift + len(dict_ta)
            dict_tb = create_t(num_t, num_row_1, num_col_1, num_col_2, shift, "tb")

            com_dict_list = [dict_t, dict_s, dict_g, dict_aa, dict_bb, dict_ab, dict_ba,
                             dict_sa, dict_sb, dict_ta, dict_tb]

            # Add variable dictionaries from com_dict_list to cumulative_dict
            for inner_dict in com_dict_list:
                for key, value in inner_dict.items():
                    cumulative_dict[key] = value

            num_var = len(cumulative_dict)
            # Create the cumulative list of commutative encoding clauses.
            cumulative_list = create_commutative_encoding_list(cumulative_dict, num_t, num_row_1, num_col_1, num_col_2)
            num_var += (num_t - 1) * (((num_row_1**2) * (num_col_2**2) * (num_col_1**2)) +
                                      ((num_row_1**3) * (num_col_1**2) * num_col_2) +
                                      (num_row_1 * (num_col_1**2) * (num_col_2**3)))

        lex_string = ""
        num_lex_clauses = 0

        if lex_order:
            # Generate vectors for lex ordering.
            vectors_col_wise, vectors_row_wise = generate_var_list(num_t, num_row_1, num_col_1,
                                                                   num_col_2, cumulative_dict)

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
        if streamlining_1:
            streamlining_var_list = generate_streamlining_v1()
            random.shuffle(streamlining_var_list)
            streamlining_parameter = streamlining_parameter_1
            streamlining_var_list = streamlining_var_list[:streamlining_parameter]
        elif streamlining_2:
            streamlining_var_list = generate_streamlining_v2(num_t, num_row_1, num_col_1,
                                                             num_col_2, streamlining_parameter_2)
        elif streamlining_3:
            streamlining_clauses, num_aux_vars = generate_streamlining_v3(cumulative_dict, num_var, num_t,
                                                                          num_row_1, num_col_1, num_col_2,
                                                                          streamlining_parameter_3)
            num_var += num_aux_vars
            cumulative_list.extend(streamlining_clauses)
            streamlining_var_list = []
        else:
            streamlining_var_list = []

        num_clauses = len(cumulative_list)
        num_clauses += len(streamlining_var_list) + num_lex_clauses

        encoding_string = f'p cnf {num_var} {num_clauses} \n'
        # Convert the clauses into CNF format, append them to
        # the encoding string and add streamlining clauses and lex string.
        encoding_string += ''.join([' '.join(map(str, innerlist)) + ' 0 \n' for innerlist in cumulative_list])
        encoding_string += streamline(streamlining_var_list, cumulative_dict)
        encoding_string += lex_string

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f'An error occurred while running encoding: {e}')

    return encoding_string, cumulative_dict
