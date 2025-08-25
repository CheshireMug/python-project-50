from gendiff.formatters.validation import validate_value


def analyze_plain_dict(dictionary, key_el):
    result_string = ''
    for el in sorted(dictionary):
        status = dictionary[el]['status']
        old_value = dictionary[el].get('old_value')
        new_value = dictionary[el].get('new_value')
        if isinstance(old_value, str):
            old_value = f'\'{old_value}\''
        if isinstance(new_value, str):
            new_value = f'\'{new_value}\''
        if isinstance(old_value, dict):
            old_value = '[complex value]'
        if isinstance(new_value, dict):
            new_value = '[complex value]'
        if status == 'nested':
            result_string += analyze_plain_dict(
                dictionary[el]['new_value'], f"{key_el}.{el}"
                )
        if status == 'added':
            result_string += \
                f'Property \'{key_el}.{el}\' \
was added with value: {validate_value(new_value)}\n'
        if status == 'removed':
            result_string += \
              f'Property \'{key_el}.{el}\' was removed\n'
        if status == 'changed':
            result_string += \
                f'Property \'{key_el}.{el}\' \
was updated. \
From {validate_value(old_value)} to {validate_value(new_value)}\n'
    return result_string


def create_plain_string(compared_data):
    result_report = ''
    for el in sorted(compared_data.keys()):
        status = compared_data[el]['status']
        new_value = compared_data[el].get('new_value')
        if status == 'nested':
            nested_str = analyze_plain_dict(new_value, el)
            result_report += nested_str
        if status == 'removed':
            result_report += f'Property \'{el}\' was removed\n'
        if status == 'added':
            if isinstance(new_value, dict):
                result_report += \
                    f'Property \'{el}\' was added \
with value: [complex value]\n'
            else:
                result_report += \
                    f'Property \'{el}\' was added \
with value {type(new_value)}\n'
    result_report = result_report.rstrip('\n')
    return result_report
