def reverse_map(value_string, value_dict):
    number_list = value_string.split()
    dict = {}
    for number in number_list:
        if number.startswith("-"):
            number = number[1:]
            for key, value in value_dict.items():
                if int(number) == value:
                    dict[f'{key}'] = 0
        else:
            for key, value in value_dict.items():
                if int(number) == value:
                    dict[f'{key}'] = 1
    return dict


def verifier(value_string, value_dict, num_t):
    result = reverse_map(value_string, value_dict)
    for key, value in result.items():
        if key.startswith("t_1"):
            sum = 0
            val_t, val_1, val_2, val_3, val_4, val_5, val_6 = key.split("_")[1:]
            for i in range(1, num_t + 1):
                sum += result[f't_{i}_{val_1}_{val_2}_{val_3}_{val_4}_{val_5}_{val_6}']
            if val_2 == val_3 and val_1 == val_5 and val_4 == val_6 and sum % 2 == 0:
                return 0
            elif (val_2 != val_3 or val_1 != val_5 or val_4 != val_6) and sum & 2 != 0:
                return 0
            else:
                return 1
