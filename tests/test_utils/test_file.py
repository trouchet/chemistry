from os import path

from src.utils.file import get_filename, extend_filename, create_folder


def test_get_filename():
    assert get_filename('/path/to/file.txt') == 'file.txt'
    assert get_filename('/another/path/to/another/file.csv') == 'file.csv'


def test_extend_filename():
    assert extend_filename('file.txt', 'new', '.') == 'file_new.txt'
    assert extend_filename('file.csv', 'extended', '.') == 'file_extended.csv'


def test_create_folder(tmp_path, capsys):
    directory_name = tmp_path / "test_directory"
    create_folder(str(directory_name))
    assert path.exists(str(directory_name))

    # Test that the function prints the correct message
    captured = capsys.readouterr()
    assert captured.out.strip() == f"Directory '{directory_name}' created!"


def test_create_folder_already_exists(tmp_path, capsys):
    directory_name = tmp_path / "test_directory"
    # Create the directory manually to simulate it already existing
    directory_name.mkdir()

    create_folder(str(directory_name))
    assert path.exists(str(directory_name))

    # Test that the function prints the correct message
    captured = capsys.readouterr()
    assert captured.out.strip() == f"Directory '{directory_name}' already exists."
