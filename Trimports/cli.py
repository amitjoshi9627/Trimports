from Trimports import trimport
from Trimports.arg_process import parse_argument


def main():
    file_path = parse_argument()
    trimport.run(file_path)


if __name__ == "__main__":
    main()
