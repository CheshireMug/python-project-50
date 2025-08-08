from gendiff.scripts.file_parser import read_files
from gendiff.scripts.gendiff import generate_diff
from gendiff.scripts.yaml_parser import read_yaml

flat_answer = '''{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}'''

requirseve_answer = '''{
    common: {
      + follow: false
        setting1: Value 1
      - setting2: 200
      - setting3: true
      + setting3: null
      + setting4: blah blah
      + setting5: {
            key5: value5
        }
        setting6: {
            doge: {
              - wow: 
              + wow: so much
            }
            key: value
          + ops: vops
        }
    }
    group1: {
      - baz: bas
      + baz: bars
        foo: bar
      - nest: {
            key: value
        }
      + nest: str
    }
  - group2: {
        abc: 12345
        deep: {
            id: 45
        }
    }
  + group3: {
        deep: {
            id: {
                number: 45
            }
        }
        fee: 100500
    }
}'''


def test_flat_gendiff():
    first_file = 'gendiff/tests/test_data/flat/file1.json'
    second_file = 'gendiff/tests/test_data/flat/file2.json'
    data = read_files(first_file, second_file)
    compared_files = generate_diff(data[0], data[1])
    assert compared_files == flat_answer


def test_flat_yaml():
    first_file = 'gendiff/tests/test_data/flat/file1.yml'
    second_file = 'gendiff/tests/test_data/flat/file2.yml'
    data = read_yaml(first_file, second_file)
    compared_files = generate_diff(data[0], data[1])
    assert compared_files == flat_answer


def test_requirseve_gendiff():
    first_file = 'gendiff/tests/test_data/requirseve/file1.json'
    second_file = 'gendiff/tests/test_data/requirseve/file2.json'
    data = read_files(first_file, second_file)
    compared_files = generate_diff(data[0], data[1])
    assert compared_files == requirseve_answer


def test_requirseve_yaml():
    first_file = 'gendiff/tests/test_data/requirseve/file1.yml'
    second_file = 'gendiff/tests/test_data/requirseve/file2.yml'
    data = read_yaml(first_file, second_file)
    compared_files = generate_diff(data[0], data[1])
    assert compared_files == requirseve_answer
