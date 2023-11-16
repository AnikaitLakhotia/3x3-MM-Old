from verifier import reverse_map
import itertools
import random


def remove_middle_element(input_string):
    """
    Remove middle element from an input string based on underscores as delimiters.

    Args:
        input_string (str): The input string to be processed.

    Returns:
        str: The modified string with middle element removed.

    Note: Input string is of format a_b_c_d, where b,c,d are numbers, and output is of format a_c_d.
    """

    # Split the input string using "_" as the delimiter
    parts = input_string.split("_")

    # Reconstruct the desired string with the first and third elements
    result = parts[0] + "_" + parts[2] + "_" + "_".join(parts[3:])

    return result


def scheme_output(matrix_dict, sat_assignment, cumulative_dict, num_t, num_row_1, num_col_2, commutative):
    """
    Compute the scheme based matrix multiplication output for two matrices.

    Args:
        matrix_dict (dict): A dictionary containing the elements of both matrices to be multiplied.
        sat_assignment (str): A space-separated string that is the output of the SAT Solver
                              if the instance given to it is satisfiable.
        cumulative_dict (dict): A dict containing all the variables in the encoding(as keys) and their
                                corresponding unique integer values.
        num_t (int): Number of 't's in each Brent equation.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.
        commutative (bool): Commutative encoding is used if True and non-commutative if False.

    Returns:
        dict: A dictionary containing the result of matrix multiplication based on the scheme.
    """

    # Reverse map variable values from value_string to dictionaries
    result = reverse_map(sat_assignment, cumulative_dict)

    g_dict = {}
    c_dict = {}
    m_dict = {}

    if not commutative:
        a_dict = {}
        b_dict = {}

        # Separate variables into a, b, and c dictionaries
        for key, value in result.items():
            if key.startswith("a"):
                a_dict[key] = value
            elif key.startswith("b"):
                b_dict[key] = value
            elif key.startswith("g"):
                g_dict[key] = value
        # Calculate 'm' values based on matrix multiplication
        for i in range(1, num_t + 1):
            a_sum = 0
            b_sum = 0

            for key, value in a_dict.items():
                if key.startswith(f'a_{i}_') and value == 1:
                    a_sum = a_sum ^ matrix_dict[remove_middle_element(f'{key}')]

            for key, value in b_dict.items():
                if key.startswith(f'b_{i}_') and value == 1:
                    b_sum = b_sum ^ matrix_dict[remove_middle_element(f'{key}')]
            m_dict[f'm_{i}'] = a_sum and b_sum

    else:
        a_dict = {}
        b_dict = {}

        # Separate variables into a, b, and c dictionaries
        for key, value in result.items():
            if key.startswith("aa"):
                a_dict[key] = value
            elif key.startswith("bb"):
                b_dict[key] = value
            elif key.startswith("ab"):
                a_dict[key] = value
            elif key.startswith("ba"):
                b_dict[key] = value
            elif key.startswith("g"):
                g_dict[key] = value

        # Calculate 'm' values based on matrix multiplication
        for i in range(1, num_t + 1):
            a_sum = 0
            b_sum = 0

            for key, value in a_dict.items():
                if (key.startswith(f'aa_{i}_') or key.startswith(f'ab_{i}_')) and value == 1:
                    key_without_middle_element = remove_middle_element(f'{key}')
                    a_sum = a_sum ^ matrix_dict[key_without_middle_element[1:]]

            for key, value in b_dict.items():
                if (key.startswith(f'bb_{i}_') or key.startswith(f'ba_{i}_')) and value == 1:
                    key_without_middle_element = remove_middle_element(f'{key}')
                    b_sum = b_sum ^ matrix_dict[key_without_middle_element[1:]]
            m_dict[f'm_{i}'] = a_sum and b_sum

    # Calculate 'c' values based on matrix multiplication
    for j in range(1, num_row_1 + 1):
        for k in range(1, num_col_2 + 1):
            g_sum = 0
            for key, value in g_dict.items():
                if key.endswith(f'{j}_{k}') and value == 1:
                    parts = key.split("_")
                    g_sum = g_sum ^ m_dict[f'm_{parts[1]}']

            c_dict[f'g_{j}_{k}'] = g_sum

    return c_dict


def generate_dicts(variables):
    """
    Generate dictionaries for all possible combinations of values(binary) for a given list of variables.

    Args:
        variables (list): List of variable names.

    Returns:
        list: List of dictionaries, each representing a combination of variable values(binary).
    """

    # Generate all possible combinations of 0 and 1 for the given variables
    value_combinations = list(itertools.product([0, 1], repeat=len(variables)))
    # Initialize an empty list to store the dictionaries
    result_dicts = []

    # Create a dictionary for each combination and add it to the result list
    for values in value_combinations:
        var_dict = dict(zip(variables, values))
        result_dicts.append(var_dict)

    random.shuffle(result_dicts)
    result_dicts = result_dicts[:10]
    return result_dicts


def multiply_matrices(matrix_a, matrix_b, num_row_1, num_col_1, num_col_2):
    """
    Multiply two matrices represented as dictionaries using standard algorithm.

    Args:
        matrix_a (dict): First matrix represented as a dictionary.
        matrix_b (dict): Second matrix represented as a dictionary.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.

    Returns:
        dict: Resulting matrix represented as a dictionary.
    """

    result_matrix = {}

    for i in range(1, num_row_1 + 1):
        for j in range(1, num_col_2 + 1):
            result = 0
            for k in range(1, num_col_1 + 1):
                result = result ^ (matrix_a[f'a_{i}_{k}'] and matrix_b[f'b_{k}_{j}'])
            result_matrix[f'g_{i}_{j}'] = result

    return result_matrix


def verifier_v2(sat_assignment, cumulative_dict, num_t, num_row_1, num_col_1, num_col_2, commutative):
    """
    Verify the correctness of matrix multiplication using the scheme by comparing it to the output of
    standard matrix multiplication for all possible matrices of orders under consideration.

    Args:
        sat_assignment (str): A space-separated string that is the output of the SAT Solver
                              if the instance given to it is satisfiable.
        cumulative_dict (dict): A dict containing all the variables in the encoding(as keys) and their
                                corresponding unique integer values.
        num_t (int): Number of 't's in each Brent equation.
        num_row_1 (int): Number of rows in the first matrix.
        num_col_1 (int): Number of columns in the first matrix.
        num_col_2 (int): Number of columns in the second matrix.
        commutative (bool): Commutative encoding is used if True and non-commutative if False.


    Returns:
        int: 1 if the scheme output matches the standard output, 0 otherwise.
    """

    var_list_a = []
    var_list_b = []

    # Generate lists of variable names for matrices A and B
    for i in range(1, num_row_1 + 1):
        for j in range(1, num_col_1 + 1):
            var_list_a.append(f'a_{i}_{j}')
    for i in range(1, num_col_1 + 1):
        for j in range(1, num_col_2 + 1):
            var_list_b.append(f'b_{i}_{j}')

    dicts_a = generate_dicts(var_list_a)
    dicts_b = generate_dicts(var_list_b)
    # Iterate through all combinations of matrix A and matrix B
    for matrix_a in dicts_a:
        for matrix_b in dicts_b:
            scheme_out = scheme_output({**matrix_a, **matrix_b}, sat_assignment, cumulative_dict,
                                       num_t, num_row_1, num_col_2, commutative)
            standard_out = multiply_matrices(matrix_a, matrix_b, num_row_1, num_col_1, num_col_2)
            # Compare the scheme output with the standard output
            if scheme_out != standard_out:
                print(scheme_out, standard_out)
                return 0

    return 1
