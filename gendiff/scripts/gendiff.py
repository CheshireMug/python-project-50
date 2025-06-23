import argparse
from gendiff.scripts.file_parser import read_files


def main():
    parser = argparse.ArgumentParser(prog='gendiff',
                    description='Compares two configuration\
files and shows a difference.')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f', '--format',
        help='set format of output'
    )
    args = parser.parse_args()
    first_file = args.first_file
    second_file = args.second_file
    data = read_files(first_file, second_file)
    print(data)
    return


if __name__ == "__main__":
    main()
