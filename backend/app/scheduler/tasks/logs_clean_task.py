from pathlib import Path
from typing import Tuple, List

from ... import MAX_LOG_FILES, MAX_LOG_FOLDER_SIZE_MB

def get_files_sorted_by_mtime(directory_path: str) -> List[Tuple[float, Path]]:
    """
    Get a list of files sorted by their modification time (oldest first) in the given directory.

    Args:
        directory_path (str): The path to the directory to manage.

    Returns:
        List[Tuple[float, Path]]: A list of tuples containing modification time and Path objects.
    """
    files = [
        (Path.getmtime(file_path), Path(file_path))
        for file_path in Path(directory_path).iterdir()
        if file_path.is_file()
    ]
    files.sort()
    return files

def manage_files(
    directory_path: str, max_files: int = MAX_LOG_FILES, max_size_mb: int = MAX_LOG_FOLDER_SIZE_MB
):
    """
    Manages the number and total size of files in a directory, deleting the oldest
    file when limits are exceeded.

    Args:
        directory_path (str): The path to the directory to manage.
        max_files (int, optional): The maximum number of files to keep. Defaults to 10.
        max_size_mb (int, optional): The maximum total size (in MB) of the directory. Defaults to 100.
    """
    files = get_files_sorted_by_mtime(directory_path)

    # Calculate total size of all files
    total_size = sum(f.stat().st_size for _, f in files)

    # Check if either limit is exceeded
    if len(files) > max_files or total_size > max_size_mb * 1024 * 1024:
        # Delete files until both limits are met (or list is empty)
        while len(files) > max_files or total_size > max_size_mb * 1024 * 1024:
            oldest_file, _ = files.pop(0)
            oldest_file.unlink()
            total_size -= oldest_file.stat().st_size

def manage_files_periodically():
    logs_path = Path.cwd() / 'logs'

    # Create the folder if it doesn't exist
    logs_path.mkdir(parents=True, exist_ok=True)
    manage_files(logs_path)

