import yaml
from yaml.loader import SafeLoader


def read_yaml(file1_name, file2_name):
    with open(file1_name) as f:
        data1 = yaml.load(f, Loader=SafeLoader)
    
    with open(file1_name) as f:
        data2 = yaml.load(f, Loader=SafeLoader)

    return data1, data2
