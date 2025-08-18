import argparse

from gendiff.scripts.file_parser import read_files
from gendiff.scripts.yaml_parser import read_yaml
from gendiff.formaters.stylish import create_stylish_string
from gendiff.formaters.plain import create_plain_string
from gendiff.formaters.json_formater import create_json_string


# Разбить на фукции поменьше
def compare_files(first_file, second_file):
    compared_data = {}
    for el2 in second_file.keys():
        new_el = {}
        if isinstance(second_file[el2], dict) and \
        el2 in first_file.keys() and \
        second_file[el2] != first_file[el2]:
            new_el['status'] = 'nested'
            new_el['new_value'] = compare_files(
                first_file[el2], second_file[el2]
                )
            compared_data[el2] = new_el
        if el2 not in first_file.keys():
            new_el['status'] = 'added'
            new_el['new_value'] = second_file[el2]
            compared_data[el2] = new_el
        if el2 in first_file.keys() and\
        second_file[el2] == first_file[el2]:
            new_el['status'] = 'unchanged'
            new_el['old_value'] = first_file[el2]
            new_el['new_value'] = second_file[el2]
            compared_data[el2] = new_el
        if not isinstance(second_file[el2], dict) and \
        el2 in first_file.keys() and \
        second_file[el2] != first_file[el2]:
            new_el['status'] = 'changed'
            new_el['old_value'] = first_file[el2]
            new_el['new_value'] = second_file[el2]
            compared_data[el2] = new_el

    for el1 in first_file.keys():
        new_el = {}
        if el1 not in second_file.keys():
            new_el['status'] = 'removed'
            new_el['old_value'] = first_file[el1]
            compared_data[el1] = new_el

    return compared_data


def generate_diff(first_file, second_file, format_name='stylish'):
    compared_data = compare_files(first_file, second_file)
    if format_name == 'stylish':
        result = create_stylish_string(compared_data)
    if format_name == 'plain':
        result = create_plain_string(compared_data)
    if format_name == 'json':
        result = create_json_string(compared_data)
    return result


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
    # Поменять срез на .endswith()
    if first_file[-5:] == '.json' and second_file[-5:] == '.json':
        data = read_files(first_file, second_file)
    elif first_file[-4:] == '.yml' and second_file[-4:] == '.yml' \
    or first_file[-5:] == '.yaml' and second_file[-5:] == '.yaml':
        data = read_yaml(first_file, second_file)
    compared_files = generate_diff(data[0], data[1], format_name=args.format)
    print(compared_files)
    return


if __name__ == "__main__":
    main()
