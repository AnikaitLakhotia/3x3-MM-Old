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
        int: 1 if the condition is satisfied, 0 otherwise.
    """

    result = reverse_map(sat_assignment, cumulative_dict)

    for key, value in result.items():
        if key.startswith(f"t_1_"):
            sum_val = 0
            val_t, val_1, val_2, val_3, val_4, val_5, val_6 = key.split("_")[1:]
            for i in range(1, num_t + 1):
                sum_val += result[f't_{i}_{val_1}_{val_2}_{val_3}_{val_4}_{val_5}_{val_6}']
            if val_2 == val_3 and val_1 == val_6 and val_4 == val_5 and sum_val % 2 == 0:
                return 0
            elif (val_2 != val_3 or val_1 != val_6 or val_4 != val_5) and sum_val % 2 != 0:
                return 0

        if commutative:
            if key.startswith(f"ta_1_") or key.startswith("tb_1_"):
                sum_val = 0
                var_str, val_t, val_1, val_2, val_3, val_4, val_5, val_6 = key.split("_")
                for i in range(1, num_t + 1):
                    sum_val += result[f'{var_str}_{i}_{val_1}_{val_2}_{val_3}_{val_4}_{val_5}_{val_6}']
                if sum_val % 2 != 0:
                    return 0

    return 1
