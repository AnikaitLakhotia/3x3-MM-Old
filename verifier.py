def reverse_map(sat_assignment, cumulative_dict):
    """
    Reverse map the values in the SAT assignment's variables to their corresponding keys(string form) in
    cumulative_dict and their respective assignments to {1,0}.

    Args:
        sat_assignment (str): A space-separated string that is the output of the SAT Solver
                              if the instance given to it is satisfiable.
        cumulative_dict (dict): A dict containing all the variables in the encoding(as keys) and their
                                corresponding unique integer values.

    Returns:
        dict: A dictionary mapping keys of cumulative_dict to 1 or 0 based on the signs of
              their respective integer values in sat_assignment.(0 if sign is '-' and 1 otherwise)
    """

    try:
        # Check the type of the 'cumulative_dict' argument
        if not isinstance(cumulative_dict, dict):
            raise TypeError(f'The cumulative_dict argument must be a dict.')

        # Check the type of the 'sat_assignment' argument
        if not isinstance(sat_assignment, str):
            raise TypeError(f'The sat_assignment argument must be a string.')

        # Check length of 'cumulative_dict' argument
        elif len(cumulative_dict) < 1:
            raise ValueError(
                f'Invalid length for cumulative_dict argument. It must be greater than or equal to 1.')

        # Check the allowed values for keys and values in 'cumulative_dict' argument
        for key, value in cumulative_dict.items():
            var_str = key[0]

            if not isinstance(key, str):
                raise TypeError(f'All keys in cumulative_dict argument must be strings, found: {key}.')

            elif not isinstance(value, int):
                raise TypeError(f'All keys in cumulative_dict argument must be integers, found: {value}.')

            elif var_str not in ["a", "b", "g", "s", "t"]:
                raise ValueError(f'Invalid key({key}) in cumulative_dict argument. It must start with'
                                 f' a, b, g, s or t.')
            elif value < 1:
                raise ValueError(f'Invalid value({value}) in cumulative_dict argument. '
                                 f'It must be greater than or equal to 1')

        if len(cumulative_dict.values()) != len(set(cumulative_dict.values())):
            raise ValueError("Duplicate values found in the cumulative_dict argument.")

        number_list = sat_assignment.split()

        # Reverse the cumulative_dict for faster lookup
        reverse_cumulative_dict = {v: k for k, v in cumulative_dict.items()}

        result_dict = {}

        for number in number_list:
            sign = -1 if number.startswith("-") else 1
            number = number.lstrip('-')
            value = int(number)

            if value in reverse_cumulative_dict:
                key = reverse_cumulative_dict[value]
                result_dict[key] = 1 if sign == 1 else 0

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f'An error occurred wile running reverse_map: {e}')

    return result_dict


def verifier(sat_assignment, cumulative_dict, num_t, commutative):
    """
    Verify if the sat_assignment obeys the rules of the Brent equations.

    Args:
        sat_assignment (str): A space-separated string of values.
        cumulative_dict (dict): A dictionary mapping keys to values.
        num_t (int): Number of 't's in each Brent equation.
        commutative (bool): Commutative encoding is used if True and non-commutative if False.

    Returns:
        int: 1 if the conditions are satisfied, 0 otherwise.
    """

    try:
        # Check the type of the 'cumulative_dict' argument
        if not isinstance(cumulative_dict, dict):
            raise TypeError(f'The cumulative_dict argument must be a dict.')

        # Check the type of the 'num_t' argument
        elif not isinstance(num_t, int):
            raise TypeError(f'The num_t argument must be an int.')

        # Check the type of the 'commutative' argument
        elif not isinstance(commutative, bool):
            raise TypeError(f'The commutative argument must be a bool.')

        # Check the type of the 'sat_assignment' argument
        elif not isinstance(sat_assignment, str):
            raise TypeError(f'The sat_assignment argument must be a string.')

        # Check value of the 'num_t' argument
        elif num_t < 2:
            raise ValueError(f'Invalid value for num_t argument. It must be greater than or equal to 2.')

        # Check the type of the 'cumulative_dict' argument
        if not isinstance(cumulative_dict, dict):
            raise TypeError(f'The cumulative_dict argument must be a dict.')

        # Check length of 'cumulative_dict' argument
        elif len(cumulative_dict) < 1:
            raise ValueError(f'Invalid length for cumulative_dict argument. It must be greater than or equal to 1.')

        # Check the allowed values for keys and values in 'cumulative_dict' argument
        for key, value in cumulative_dict.items():
            var_str = key[:2]

            if not isinstance(key, str):
                raise TypeError(f'All keys in cumulative_dict argument must be strings, found: {key}.')

            elif not isinstance(value, int):
                raise TypeError(f'All keys in cumulative_dict argument must be integers, found: {value}.')

            elif var_str not in ["aa", "a_", "bb", "b_", "ab", "ba", "g_", "s_", "sa", "sb", "t_", "ta", "tb"]:
                raise ValueError(f'Invalid key({key}) in cumulative_dict argument. It must start with'
                                 f' aa, a, bb, b, ab, ba, s, sa, sb, t, ta, or tb.')

            elif value < 1:
                raise ValueError(f'Invalid value({value}) in cumulative_dict argument. '
                                 f'It must be greater than or equal to 1')

        if len(cumulative_dict.values()) != len(set(cumulative_dict.values())):
            raise ValueError("Duplicate values found in the cumulative_dict argument.")

        result = reverse_map(sat_assignment, cumulative_dict)

        for key, value in result.items():
            if key.startswith(f"t_1_"):
                sum_val = 0
                val_t, val_1, val_2, val_3, val_4, val_5, val_6 = key.split("_")[1:]
                for i in range(1, num_t + 1):
                    sum_val += result[f't_{i}_{val_1}_{val_2}_{val_3}_{val_4}_{val_5}_{val_6}']

                    if result[f't_{i}_{val_1}_{val_2}_{val_3}_{val_4}_{val_5}_{val_6}'] != result[
                       f's_{i}_{val_1}_{val_2}_{val_3}_{val_4}'] and result[f'g_{i}_{val_5}_{val_6}']:
                        return 0

                    elif not commutative:
                        if result[f's_{i}_{val_1}_{val_2}_{val_3}_{val_4}'] != (
                           result[f'a_{i}_{val_1}_{val_2}'] and result[f'b_{i}_{val_3}_{val_4}']):
                            return 0

                    elif result[f's_{i}_{val_1}_{val_2}_{val_3}_{val_4}'] != (
                         result[f'aa_{i}_{val_1}_{val_2}'] and result[f'bb_{i}_{val_3}_{val_4}']) ^ (
                         result[f'ab_{i}_{val_3}_{val_4}'] and result[f'ba_{i}_{val_1}_{val_2}']):
                        return 0

                if val_2 == val_3 and val_1 == val_5 and val_4 == val_6 and sum_val % 2 == 0:
                    return 0

                elif (val_2 != val_3 or val_1 != val_5 or val_4 != val_6) and sum_val % 2 != 0:
                    return 0

            if commutative:
                if key.startswith(f"ta_1_") or key.startswith("tb_1_"):
                    sum_val = 0
                    var_str, val_t, val_1, val_2, val_3, val_4, val_5, val_6 = key.split("_")
                    for i in range(1, num_t + 1):
                        sum_val += result[f'{var_str}_{i}_{val_1}_{val_2}_{val_3}_{val_4}_{val_5}_{val_6}']

                        if result[f'{var_str}_{i}_{val_1}_{val_2}_{val_3}_{val_4}_{val_5}_{val_6}'] != result[
                           f's{var_str[1:]}_{i}_{val_1}_{val_2}_{val_3}_{val_4}'] and result[f'g_{i}_{val_5}_{val_6}']:
                            return 0

                        elif key.startswith(f"ta_1_"):
                            if val_1 != val_3 or val_2 != val_4:
                                if result[f's{var_str[1:]}_{i}_{val_1}_{val_2}_{val_3}_{val_4}'] != (
                                   result[f'aa_{i}_{val_1}_{val_2}'] and result[f'ba_{i}_{val_3}_{val_4}']) ^ (
                                   result[f'aa_{i}_{val_3}_{val_4}'] and result[f'ba_{i}_{val_1}_{val_2}']):
                                    return 0

                            else:
                                if result[f's{var_str[1:]}_{i}_{val_1}_{val_2}_{val_3}_{val_4}'] != (
                                        result[f'aa_{i}_{val_1}_{val_2}'] and result[f'ba_{i}_{val_3}_{val_4}']):
                                    return 0

                        elif key.startswith("tb_1_"):
                            if val_1 != val_3 or val_2 != val_4:
                                if result[f's{var_str[1:]}_{i}_{val_1}_{val_2}_{val_3}_{val_4}'] != (
                                   result[f'ab_{i}_{val_1}_{val_2}'] and result[f'bb_{i}_{val_3}_{val_4}']) ^ (
                                   result[f'ab_{i}_{val_3}_{val_4}'] and result[f'bb_{i}_{val_1}_{val_2}']):
                                    return 0

                            else:
                                if result[f's{var_str[1:]}_{i}_{val_1}_{val_2}_{val_3}_{val_4}'] != (
                                   result[f'ab_{i}_{val_1}_{val_2}'] and result[f'bb_{i}_{val_3}_{val_4}']):
                                    return 0

                    if sum_val % 2 != 0:
                        return 0

    except Exception as e:
        # Handle any unexpected exceptions
        raise RuntimeError(f'An error occurred wile running verifier: {e}')

    return 1
