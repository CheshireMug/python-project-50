from gendiff.scripts.file_parser import read_files
from gendiff.scripts.gendiff import generate_diff

answer = '''{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}'''


def test_gendiff():
    first_file = 'gendiff/tests/test_data/file1.json'
    second_file = 'gendiff/tests/test_data/file2.json'
    data = read_files(first_file, second_file)
    compared_files = generate_diff(data[0], data[1])
    assert compared_files == answer
