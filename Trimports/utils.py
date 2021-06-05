def get_file_lines(file_path):
    with open(file_path) as file:
        lines = file.readlines()
    return lines


def write_file(file_path, file_lines):
    with open(file_path, "w") as f:
        f.writelines(file_lines)
