import os
import sys

def is_scheme_new():
    def get_all_directories(path):
        directory_paths = [os.path.join(path, entry) for entry in os.listdir(path) if os.path.isdir(os.path.join(path, entry))]
        return directory_paths

    def compare_directory_contents(directory_path, reference_file_path):
        with open(reference_file_path, 'r') as reference_file:
            reference_content = reference_file.read()

            for root, dirs, files in os.walk(directory_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)

                    with open(file_path, 'r') as current_file:
                        current_content = current_file.read()
                        if current_content == reference_content:
                            print(f"Match found in {file_name}")
                            return True
        return False

    base_path = "/home/ubuntu/3x3-MM/Pseudo-Boolean"
    directory_path = "schemes"
    full_path = os.path.join(base_path, directory_path)
    _, reference_file_path = sys.argv
    reference_file_path = base_path + "/" + reference_file_path
    print(reference_file_path)

    directories = get_all_directories(full_path)

    for directory in directories:
        if compare_directory_contents(directory, reference_file_path):
            return False
    return True
        
if is_scheme_new():
    print("This generate scheme is new!")
