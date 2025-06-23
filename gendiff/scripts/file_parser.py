import json


def read_files(file1_name, file2_name):
    with open(file1_name, 'r') as file1:
        data1 = json.load(file1)


    with open(file2_name, 'r') as file2:
        data2 = json.load(file2)

    return data1, data2
