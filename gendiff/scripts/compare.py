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
