from gendiff.formaters.json_formater import create_json_string
from gendiff.formaters.plain import create_plain_string
from gendiff.formaters.stylish import create_stylish_string
from gendiff.scripts.compare import compare_files


def generate_diff(first_file, second_file, format_name='stylish'):
    compared_data = compare_files(first_file, second_file)
    if format_name == 'stylish':
        result = create_stylish_string(compared_data)
    if format_name == 'plain':
        result = create_plain_string(compared_data)
    if format_name == 'json':
        result = create_json_string(compared_data)
    return result
