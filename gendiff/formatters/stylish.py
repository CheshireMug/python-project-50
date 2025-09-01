from gendiff.scripts.validation import validate_value


def create_dict(dictionary, indent=0):
    indent_str = '    ' * indent
    result_string = '{\n'
    for key, value in dictionary.items():
        formatted_value = (
            create_dict(value, indent + 1)
            if isinstance(value, dict)
            else validate_value(value)
        )
        result_string += f'{indent_str}    {key}: {formatted_value}\n'
    result_string += f'{indent_str}}}'
    return result_string


def format_line(indent_str, sign, key, value, indent):
    if isinstance(value, dict):
        dict_str = create_dict(value, indent + 1)
        return f'{indent_str}  {sign} {key}: {dict_str}\n'
    return f'{indent_str}  {sign} {key}: {validate_value(value)}\n'


def stylish_string_conditions(
          result_report, status, new_value, old_value,
          indent_str, indent, el
          ):
    if status == 'nested':
        nested_str = create_stylish_string(new_value, indent + 1)
        return result_report + f'{indent_str}    {el}: {nested_str}\n'

    if status == 'removed':
        return result_report \
            + format_line(indent_str, '-', el, old_value, indent)

    if status == 'unchanged':
        return result_report \
            + format_line(indent_str, ' ', el, new_value, indent)

    if status == 'changed':
        result_report += format_line(indent_str, '-', el, old_value, indent)
        result_report += format_line(indent_str, '+', el, new_value, indent)
        return result_report

    if status == 'added':
        return result_report + \
            format_line(indent_str, '+', el, new_value, indent)

    return result_report


def stylish_string_cycle(
        result_report, sorted_keys, compared_data, indent_str, indent
        ):
    for el in sorted_keys:
        status = compared_data[el]['status']
        old_value = compared_data[el].get('old_value')
        new_value = compared_data[el].get('new_value')
        result_report = stylish_string_conditions(
            result_report, status, new_value, old_value,
            indent_str, indent, el
        )
    return result_report


def create_stylish_string(compared_data, indent=0):
    indent_str = ' ' * 4 * indent
    result_report = '{\n'
    sorted_keys = sorted(compared_data.keys())
    result_report = stylish_string_cycle(
        result_report, sorted_keys, compared_data, indent_str, indent
        )
    result_report += f'{indent_str}}}'
    return result_report
