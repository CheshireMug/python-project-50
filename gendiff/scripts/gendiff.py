import argparse
from gendiff.scripts.file_parser import read_files


def generate_diff(first_file, second_file):
    compared_data = []
    first_file_data = first_file
    second_file_data = second_file
    for el2 in second_file_data.keys():
        new_el = {}
        if el2 not in first_file_data.keys():
            new_el['status'] = 'added'
            new_el['new_value'] = second_file_data[el2]
            compared_data.append({el2: new_el})
        if el2 in first_file_data.keys() and\
        second_file_data[el2] == first_file_data[el2]:
            new_el['status'] = 'unchanged'
            new_el['old_value'] = first_file_data[el2]
            new_el['new_value'] = second_file_data[el2]
            compared_data.append({el2: new_el})
        if el2 in first_file_data.keys() and\
        second_file_data[el2] != first_file_data[el2]:
            new_el['status'] = 'changed'
            new_el['old_value'] = first_file_data[el2]
            new_el['new_value'] = second_file_data[el2]
            compared_data.append({el2: new_el})
    for el1 in first_file_data.keys():
        new_el = {}
        if el1 not in second_file_data.keys():
            new_el['status'] = 'removed'
            new_el['old_value'] = first_file_data[el1]
            compared_data.append({el1: new_el})
    compared_data = sorted(compared_data,\
                            key=lambda x: sorted(x.keys())[0] if x else '')
    result_report = '{\n'
    for el in compared_data:
        for sideEl in el:
            if el[sideEl]['status'] == 'removed':
                result_report += \
                f'  - {sideEl}: {el[sideEl]['old_value']}\n'
            if el[sideEl]['status'] == 'unchanged':
                result_report += \
                f'    {sideEl}: {el[sideEl]['new_value']}\n'
            if el[sideEl]['status'] == 'changed':
                result_report += \
                f'  - {sideEl}: {el[sideEl]['old_value']}\n'
                result_report += \
                f'  + {sideEl}: {el[sideEl]['new_value']}\n'
            if el[sideEl]['status'] == 'added':
                result_report += \
                f'  + {sideEl}: {el[sideEl]['new_value']}\n'
    result_report += '}'
    return result_report
        
        
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
    compared_files = generate_diff(data[0], data[1])
    print(compared_files)
    return


if __name__ == "__main__":
    main()
