from gendiff.formaters.validation import validate_value


def create_dict(dictionary, indent=0):
    indent_str = '    ' * indent
    result_string = '{\n'
    for key, value in dictionary.items():
        if isinstance(value, dict):
            result_string += \
                f'{indent_str}    {key}: {create_dict(value, indent + 1)}\n'
        else:
            result_string += \
                f'{indent_str}    {key}: {validate_value(value)}\n'
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
                result_report += \
                    f'{indent_str}  - {el}: {validate_value(old_value)}\n'
        if status == 'unchanged':
            if isinstance(new_value, dict):
                dict_str = create_dict(new_value, indent + 1)
                result_report += f'{indent_str}    {el}: {dict_str}\n'
            else:
                result_report += \
                    f'{indent_str}    {el}: {validate_value(new_value)}\n'
        if status == 'changed':
            if isinstance(old_value, dict):
                dict_str = create_dict(old_value, indent + 1)
                result_report += f'{indent_str}  - {el}: {dict_str}\n'
            else:
                result_report += \
                    f'{indent_str}  - {el}: {validate_value(old_value)}\n'
            if isinstance(new_value, dict):
                dict_str = create_dict(new_value, indent + 1)
                result_report += f'{indent_str}  + {el}: {dict_str}\n'
            else:
                result_report += \
                    f'{indent_str}  + {el}: {validate_value(new_value)}\n'
        if status == 'added':
            if isinstance(new_value, dict):
                dict_str = create_dict(new_value, indent + 1)
                result_report += f'{indent_str}  + {el}: {dict_str}\n'
            else:
                result_report += \
                    f'{indent_str}  + {el}: {validate_value(new_value)}\n'
    result_report += f'{indent_str}}}'
    return result_report
