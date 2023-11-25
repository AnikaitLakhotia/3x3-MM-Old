import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import re
import os
matplotlib.use('Agg')


def get_absolute_directories(directory):
    absolute_directories = [os.path.join(directory, d) for d in os.listdir(
        directory) if os.path.isdir(os.path.join(directory, d))]
    return absolute_directories


def extract_multiplications(file_path):
    file_path = file_path.split("/")
    expirement_information = file_path[-1]
    specific_expirement_information = expirement_information.split("_")
    return specific_expirement_information[2]


def get_timing_information(file_path):
    file_path_portions = file_path.split("/")
    file_path_portions_for_timings = file_path_portions[-1]
    timing_information_file = file_path + "/" + \
        file_path_portions_for_timings + "_assignment.txt"
    file_type = ""
    with open(timing_information_file) as file:
        for line in file:
            if line.startswith('s'):
                value = line.split()[1]
                file_type = value
    if file_type == "UNKNOWN" or file_type == "UNSATISFIABLE":
        return 0
    with open(timing_information_file, 'r') as file:
        for line in file:
            match = re.match(r'c total solve time (\d+\.\d+) s', line)
            if match:
                total_solve_time = float(match.group(1))
                return total_solve_time


def get_multiplication_information(file_path):
    file_path_portions = file_path.split("/")
    file_path_portions_for_timings = file_path_portions[-1]
    return file_path_portions_for_timings


def plot_data(x_axis, y_axis, title, information):
    multiplications = []
    solving_time = []
    data_point_information = []

    for file_path in information:
        multiplications.append(extract_multiplications(file_path))
        solving_time.append(get_timing_information(file_path))
        data_point_information.append(
            get_multiplication_information(file_path))

    # Sort data based on x-axis values
    sorted_data = sorted(zip(multiplications, solving_time,
                         data_point_information), key=lambda x: x[0])
    multiplications, solving_time, data_point_information = zip(*sorted_data)

    colors = plt.cm.viridis(np.linspace(0, 1, len(multiplications)))

    for i, txt in enumerate(data_point_information):
        plt.scatter(multiplications[i], solving_time[i], c=[
                    colors[i]], label=f'{i+1}: {txt}')
        plt.annotate(f'({multiplications[i]}, {solving_time[i]})', (
            multiplications[i], solving_time[i]), fontsize=8, color=colors[i], rotation=45)

    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(title)

    plt.legend(title='Data Points')

    plt.savefig(f'{title}.png')

    plt.close()


directory_path = '/home/a58kapoo/research/3x3-MM/Pseudo-Boolean/opb'

data_file_paths = get_absolute_directories(directory_path)

plot_data("Multiplications", "Total Solve Time (s)",
          "Test Plot", data_file_paths)
