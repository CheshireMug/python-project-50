import argparse

from gendiff.scripts.file_parser import read_files
from gendiff.scripts.genetator import generate_diff
from gendiff.scripts.yaml_parser import read_yaml


def main():
    parser = argparse.ArgumentParser(prog='gendiff',
                    description='Compares two configuration\
files and shows a difference.')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f', '--format',
        default='stylish',
        help='set format of output'
    )
    args = parser.parse_args()
    first_file = args.first_file
    second_file = args.second_file
    if first_file.endswith('.json') and second_file.endswith('.json'):
        data = read_files(first_file, second_file)
    elif first_file.endswith('.yml') and second_file.endswith('.yml') \
    or first_file.endswith('.yaml') and second_file.endswith('.yaml'):
        data = read_yaml(first_file, second_file)
    compared_files = generate_diff(data[0], data[1], format_name=args.format)
    print(compared_files)
    return


if __name__ == "__main__":
    main()
