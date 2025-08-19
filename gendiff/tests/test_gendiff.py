import pytest

from gendiff.scripts.file_parser import read_files
from gendiff.scripts.gendiff import generate_diff
from gendiff.scripts.yaml_parser import read_yaml


# Перенести в фикстуры
@pytest.fixture
def flat_answer():
    with open("gendiff/tests/fixtures/flat_fixture.txt",
               "r", encoding="utf-8") as f:
        data = f.read()
    return data


@pytest.fixture
def requirseve_answer():
    with open("gendiff/tests/fixtures/requirseve_fixture.txt",
               "r", encoding="utf-8") as f:
        data = f.read()
    return data


@pytest.fixture
def plain_answer():
    with open("gendiff/tests/fixtures/plain_fixture.txt",
               "r", encoding="utf-8") as f:
        data = f.read()
    return data


@pytest.fixture
def json_answer():
    with open("gendiff/tests/fixtures/json_fixture.json",
               "r", encoding="utf-8") as f:
        data = f.read()
    return data


# Для путей использовать библиотеку pathlib либо os.path.join
def test_flat_gendiff(flat_answer):
    first_file = 'gendiff/tests/test_data/flat/file1.json'
    second_file = 'gendiff/tests/test_data/flat/file2.json'
    data = read_files(first_file, second_file)
    compared_files = generate_diff(data[0], data[1])
    assert compared_files == flat_answer


def test_flat_yaml(flat_answer):
    first_file = 'gendiff/tests/test_data/flat/file1.yml'
    second_file = 'gendiff/tests/test_data/flat/file2.yml'
    data = read_yaml(first_file, second_file)
    compared_files = generate_diff(data[0], data[1])
    assert compared_files == flat_answer


def test_requirseve_gendiff(requirseve_answer):
    first_file = 'gendiff/tests/test_data/requirseve/file1.json'
    second_file = 'gendiff/tests/test_data/requirseve/file2.json'
    data = read_files(first_file, second_file)
    compared_files = generate_diff(data[0], data[1])
    assert compared_files == requirseve_answer


def test_requirseve_yaml(requirseve_answer):
    first_file = 'gendiff/tests/test_data/requirseve/file1.yml'
    second_file = 'gendiff/tests/test_data/requirseve/file2.yml'
    data = read_yaml(first_file, second_file)
    compared_files = generate_diff(data[0], data[1])
    assert compared_files == requirseve_answer


def test_plain_gendiff(plain_answer):
    first_file = 'gendiff/tests/test_data/requirseve/file1.json'
    second_file = 'gendiff/tests/test_data/requirseve/file2.json'
    data = read_files(first_file, second_file)
    compared_files = generate_diff(data[0], data[1], 'plain')
    assert compared_files == plain_answer


def test_plain_yaml(plain_answer):
    first_file = 'gendiff/tests/test_data/requirseve/file1.yml'
    second_file = 'gendiff/tests/test_data/requirseve/file2.yml'
    data = read_yaml(first_file, second_file)
    compared_files = generate_diff(data[0], data[1], 'plain')
    assert compared_files == plain_answer


def test_json_formater_json(json_answer):
    first_file = 'gendiff/tests/test_data/requirseve/file1.json'
    second_file = 'gendiff/tests/test_data/requirseve/file2.json'
    data = read_files(first_file, second_file)
    compared_files = generate_diff(data[0], data[1], 'json')
    assert compared_files == json_answer


def test_json_formater_yaml(json_answer):
    first_file = 'gendiff/tests/test_data/requirseve/file1.yml'
    second_file = 'gendiff/tests/test_data/requirseve/file2.yml'
    data = read_yaml(first_file, second_file)
    compared_files = generate_diff(data[0], data[1], 'json')
    assert compared_files == json_answer
