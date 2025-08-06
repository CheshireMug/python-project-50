import argparse

from gendiff.scripts.file_parser import read_files
from gendiff.scripts.yaml_parser import read_yaml


def validate_value(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    return value



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


def create_dict(dictionary, indent=0):
    indent_str = '    ' * indent
    result_string = '{\n'
    for key, value in dictionary.items():
        if isinstance(value, dict):
            result_string += f'{indent_str}    {key}: {create_dict(value, indent + 1)}\n'
        else:
            result_string += f'{indent_str}    {key}: {validate_value(value)}\n'
    result_string += f'{indent_str}}}'
    return result_string


def create_stylish_string(compared_data, indent=0):
    indent_str = '    ' * indent
    result_report = '{\n'
    for el in sorted(compared_data.keys()):
        status = compared_data[el]['status']
        old_value = compared_data[el].get('old_value')
        new_value = compared_data[el].get('new_value')
        if status == 'nested':
            nested_str = create_stylish_string(new_value, indent + 1)
            result_report += f'{indent_str}    {el}: {nested_str}\n'
        if status == 'removed':
            if isinstance(old_value, dict):
                dict_str = create_dict(old_value, indent + 1)
                result_report += f'{indent_str}  - {el}: {dict_str}\n'
            else:
                result_report += f'{indent_str}  - {el}: {validate_value(old_value)}\n'
        if status == 'unchanged':
            if isinstance(new_value, dict):
                dict_str = create_dict(new_value, indent + 1)
                result_report += f'{indent_str}    {el}: {dict_str}\n'
            else:
                result_report += f'{indent_str}    {el}: {validate_value(new_value)}\n'
        if status == 'changed':
            if isinstance(old_value, dict):
                dict_str = create_dict(old_value, indent + 1)
                result_report += f'{indent_str}  - {el}: {dict_str}\n'
            else:
                result_report += f'{indent_str}  - {el}: {validate_value(old_value)}\n'
            if isinstance(new_value, dict):
                dict_str = create_dict(new_value, indent + 1)
                result_report += f'{indent_str}  + {el}: {dict_str}\n'
            else:
                result_report += f'{indent_str}  + {el}: {validate_value(new_value)}\n'
        if status == 'added':
            if isinstance(new_value, dict):
                dict_str = create_dict(new_value, indent + 1)
                result_report += f'{indent_str}  + {el}: {dict_str}\n'
            else:
                result_report += f'{indent_str}  + {el}: {validate_value(new_value)}\n'
    result_report += f'{indent_str}}}'
    return result_report


def generate_diff(first_file, second_file, format_name='stylish'):
    compared_data = compare_files(first_file, second_file)
    if format_name == 'stylish':
        result = create_stylish_string(compared_data)
    return result
    # result_report = '{\n'
    # for el in compared_data:
    #     for sideEl in el:
    #         if el[sideEl]['status'] == 'removed':
    #             result_report += \
    #           f'  - {sideEl}: {validate_value(el[sideEl]['old_value'])}\n'
    #         if el[sideEl]['status'] == 'unchanged':
    #             result_report += \
    #             f'    {sideEl}: {validate_value(el[sideEl]['new_value'])}\n'
    #         if el[sideEl]['status'] == 'changed':
    #             result_report += \
    #             f'  - {sideEl}: {validate_value(el[sideEl]['old_value'])}\n'
    #             result_report += \
    #             f'  + {sideEl}: {validate_value(el[sideEl]['new_value'])}\n'
    #         if el[sideEl]['status'] == 'added':
    #             result_report += \
    #             f'  + {sideEl}: {validate_value(el[sideEl]['new_value'])}\n'
    # result_report += '}'
    # return result_report
        
        
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
    if first_file[-5:] == '.json' and second_file[-5:] == '.json':
        data = read_files(first_file, second_file)
    elif first_file[-4:] == '.yml' and second_file[-4:] == '.yml' \
    or first_file[-5:] == '.yaml' and second_file[-5:] == '.yaml':
        data = read_yaml(first_file, second_file)
    compared_files = generate_diff(data[0], data[1])
    print(compared_files)
    return


if __name__ == "__main__":
    main()
