from gendiff.scripts.file_parser import read_files
from gendiff.scripts.gendiff import generate_diff
from gendiff.scripts.yaml_parser import read_yaml

# Перенести в фикстуры
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


plain_answer = '''Property 'common.follow' was added with value: false
Property 'common.setting2' was removed
Property 'common.setting3' was updated. From true to null
Property 'common.setting4' was added with value: 'blah blah'
Property 'common.setting5' was added with value: [complex value]
Property 'common.setting6.doge.wow' was updated. From '' to 'so much'
Property 'common.setting6.ops' was added with value: 'vops'
Property 'group1.baz' was updated. From 'bas' to 'bars'
Property 'group1.nest' was updated. From [complex value] to 'str'
Property 'group2' was removed
Property 'group3' was added with value: [complex value]'''


json_answer = '''{"common": {"status": "nested", "new_value": {"follow": {"status": "added", "new_value": false}, "setting1": {"status": "unchanged", "old_value": "Value 1", "new_value": "Value 1"}, "setting3": {"status": "changed", "old_value": true, "new_value": null}, "setting4": {"status": "added", "new_value": "blah blah"}, "setting5": {"status": "added", "new_value": {"key5": "value5"}}, "setting6": {"status": "nested", "new_value": {"key": {"status": "unchanged", "old_value": "value", "new_value": "value"}, "ops": {"status": "added", "new_value": "vops"}, "doge": {"status": "nested", "new_value": {"wow": {"status": "changed", "old_value": "", "new_value": "so much"}}}}}, "setting2": {"status": "removed", "old_value": 200}}}, "group1": {"status": "nested", "new_value": {"foo": {"status": "unchanged", "old_value": "bar", "new_value": "bar"}, "baz": {"status": "changed", "old_value": "bas", "new_value": "bars"}, "nest": {"status": "changed", "old_value": {"key": "value"}, "new_value": "str"}}}, "group3": {"status": "added", "new_value": {"deep": {"id": {"number": 45}}, "fee": 100500}}, "group2": {"status": "removed", "old_value": {"abc": 12345, "deep": {"id": 45}}}}'''


# Для путей использовать библиотеку pathlib либо os.path.join
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


def test_plain_gendiff():
    first_file = 'gendiff/tests/test_data/requirseve/file1.json'
    second_file = 'gendiff/tests/test_data/requirseve/file2.json'
    data = read_files(first_file, second_file)
    compared_files = generate_diff(data[0], data[1], 'plain')
    assert compared_files == plain_answer


def test_plain_yaml():
    first_file = 'gendiff/tests/test_data/requirseve/file1.yml'
    second_file = 'gendiff/tests/test_data/requirseve/file2.yml'
    data = read_yaml(first_file, second_file)
    compared_files = generate_diff(data[0], data[1], 'plain')
    assert compared_files == plain_answer


def test_json_formater_json():
    first_file = 'gendiff/tests/test_data/requirseve/file1.json'
    second_file = 'gendiff/tests/test_data/requirseve/file2.json'
    data = read_files(first_file, second_file)
    compared_files = generate_diff(data[0], data[1], 'json')
    assert compared_files == json_answer


def test_json_formater_yaml():
    first_file = 'gendiff/tests/test_data/requirseve/file1.yml'
    second_file = 'gendiff/tests/test_data/requirseve/file2.yml'
    data = read_yaml(first_file, second_file)
    compared_files = generate_diff(data[0], data[1], 'json')
    assert compared_files == json_answer
