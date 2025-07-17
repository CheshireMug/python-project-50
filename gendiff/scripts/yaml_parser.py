import yaml
from yaml.loader import SafeLoader


file1_path = 'gendiff/test_data/file1.yml'
file2_path = 'gendiff/test_data/file2.yml'


def read_yaml_files(file1_name, file2_name):
    with open(file1_name) as f:
        data1 = yaml.load(f, Loader=SafeLoader)
    
    with open(file1_name) as f:
        data2 = yaml.load(f, Loader=SafeLoader)

    return data1, data2

print(read_yaml_files(file1_path, file2_path))
