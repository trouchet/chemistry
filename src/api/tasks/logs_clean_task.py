from os import getcwd, path

from src.api.utils.logs import manage_files


def manage_files_periodically():
    logs_path = path.join(getcwd(), 'logs')

    # Create the folder if it doesn't exist
    logs_path.mkdir(parents=True, exist_ok=True)
    manage_files(logs_path)
