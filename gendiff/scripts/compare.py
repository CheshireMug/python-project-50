# Разбить на фукции поменьше
def compare_conditions(key, first_file, second_file, new_el):
    if key in first_file and key in second_file:
        if isinstance(first_file[key], dict) and isinstance(
            second_file[key], dict
            ):
            new_el['status'] = 'nested'
            new_el['new_value'] = compare_files(
                first_file[key], second_file[key]
                )
        elif first_file[key] == second_file[key]:
            new_el['status'] = 'unchanged'
            new_el['old_value'] = first_file[key]
            new_el['new_value'] = second_file[key]
        else:
            new_el['status'] = 'changed'
            new_el['old_value'] = first_file[key]
            new_el['new_value'] = second_file[key]
    elif key in first_file:
        new_el['status'] = 'removed'
        new_el['old_value'] = first_file[key]
    else:  # key in second_file
        new_el['status'] = 'added'
        new_el['new_value'] = second_file[key]
    return new_el


def compare_cycle(first_file, second_file, all_keys, compared_data):
    for key in all_keys:
        new_el = {}
        compared_data[key] = compare_conditions(
            key, first_file, second_file, new_el
            )
    return compared_data


def compare_files(first_file, second_file):
    compared_data = {}
    all_keys = sorted(set(first_file.keys()) | set(second_file.keys()))
    compared_data = compare_cycle(
        first_file, second_file, all_keys, compared_data
        )
    return compared_data
