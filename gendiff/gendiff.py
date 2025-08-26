import argparse
import os

from gendiff.formatters.json_formater import create_json_string
from gendiff.formatters.plain import create_plain_string
from gendiff.formatters.stylish import create_stylish_string
from gendiff.scripts.compare import compare_files
from gendiff.scripts.file_parser import read_files
from gendiff.scripts.yaml_parser import read_yaml


def generate_diff(first_file, second_file, format_name='stylish'):
    if isinstance(first_file, str) and isinstance(second_file, str):
        _, ext1 = os.path.splitext(first_file)
        _, ext2 = os.path.splitext(second_file)

        if ext1 in (".yml", ".yaml") and ext2 in (".yml", ".yaml"):
            data1, data2 = read_yaml(first_file, second_file)
        elif ext1 == ".json" and ext2 == ".json":
            data1, data2 = read_files(first_file, second_file)
        else:
            raise ValueError("Unsupported file format")
    else:
        data1, data2 = first_file, second_file

    compared_data = compare_files(data1, data2)

    if format_name == "stylish":
        return create_stylish_string(compared_data)
    if format_name == "plain":
        return create_plain_string(compared_data)
    if format_name == "json":
        return create_json_string(compared_data)

    raise ValueError(f"Unknown format: {format_name}")


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

    compared_files = generate_diff(
        args.first_file, args.second_file, format_name=args.format
        )
    print(compared_files)
    return


if __name__ == "__main__":
    main()
