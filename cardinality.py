import subprocess

def k_constraint(var_list, num_var, k, at_most_at_least_only_k):
    """
    if at_most_at_least_only_k == -1:
        then encode at least k => a + b + ... + z >= k
    if at_most_at_least_only_k == 0:
        then encode only k k => a + b + ... + z == k
    if at_most_at_least_only_k == 1:
        then encode at most k => a + b + ... + z >= -k 
    """
    if at_most_at_least_only_k < -1 or at_most_at_least_only_k > 1:
        raise Exception("Invalid value for at_most_at_least_only_k")
    
    temp_cardinality_file = "temp_cardinality_file.txt"
    variable_set = set(var_list)
    constraint_literals = []
    unit_clauses = []
    unit_clauses_set = set()

    for variable in range(1, num_var + 1):
        if variable not in variable_set:
            unit_clauses_set.add(str(variable))
            unit_clauses.append(variable)
        else:
            constraint_literals.append(f"1 x{variable} ")

    with open(temp_cardinality_file, 'w+') as file:
        file.write(f"* #variable= {num_var} #constraint= {len(unit_clauses) + 1}\n*\n")
        for unit in unit_clauses:
            file.write(f"1 x{unit} = 0;\n")

        operation = ""

        if at_most_at_least_only_k == -1:
            operation = f">= {k};"
        elif at_most_at_least_only_k == 0:
            operation = f"== {k};"
        else:
            operation = f">= -{k};"
        constraint_literals.append(operation)

        k_constraint = "".join(constraint_literals)
        file.write(k_constraint)

    command = ['./pblib/build/pbencoder', temp_cardinality_file]
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

    if result.returncode == 0:
        with open('new_constraints.cnf', 'w') as output_file:
            output_file.write(result.stdout)
        print("Command executed successfully.")
    else:
        print("Error executing the command.")
        print(result.stderr)

    with open('new_constraints.cnf', 'r') as file:
        file = file.readlines()
        cnf_constraints = []
        for line in file:
            curr_constraint = line[:]
            line = line[:-1]
            line = line.split(" ")
            if line[0][0] == '-' and line[0][1:] in unit_clauses_set:
                continue
            else:
                cnf_constraints.append(curr_constraint)

    inital_header = cnf_constraints[0]
    inital_header = inital_header.split(" ")
    inital_header[-1] = str(len(cnf_constraints) - 1)
    inital_header.append("\n")
    cnf_constraints[0] = " ".join(inital_header)
    
    with open('new_constraints.cnf', 'w') as file:
        for curr_constraint in cnf_constraints:
            file.write(curr_constraint)

k_constraint([1, 9, 2, 4, 5,3,22,24,50,99, 7], 102, 5, -1)
