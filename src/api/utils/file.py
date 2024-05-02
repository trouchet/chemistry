from os import path, makedirs
import os

def get_filename(filename: str) -> str:
    '''
    Retorna o nome do arquivo dado o caminho completo do arquivo.
    '''
    return path.basename(filename)


def extend_filename(filename: str, token: str, delimiter: str = '.') -> str:
    '''
    Estende o nome do arquivo adicionando um token antes da extensão,
    mantendo o nome original e a extensão.
    '''

    extension = filename.split(delimiter)[-1]
    body = filename.split(delimiter)[:-1]

    new_filename = delimiter.join(body) + '_' + token + delimiter + extension

    return new_filename


def create_folder(directory_name: str) -> str:
    '''
    Cria um diretório com o nome fornecido se ele não existir, e exibe
    uma mensagem indicando se o diretório foi criado ou se já existe.
    '''
    from os import path

    if not path.exists(directory_name):
        makedirs(directory_name)
        print(f"Directory '{directory_name}' created!")
    else:
        print(f"Directory '{directory_name}' already exists.")

def get_file_size(file_path):
    """
    Gets the size of a file in bytes using os.path.getsize.

    Args:
        file_path (str): The path to the file.

    Returns:
        int: The size of the file in bytes.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    try:
        return os.path.getsize(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")