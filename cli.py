from Trimports import trimport
from Trimports.arg_process import parse_argument

if __name__ == "__main__":
    file_path = parse_argument()
    trimport.run(file_path)
