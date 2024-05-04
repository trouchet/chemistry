import os

from src.api.constants import MAX_LOG_FILES, MAX_LOG_FOLDER_SIZE_MB

import os
from pathlib import Path

def manage_files(
    directory_path, 
    max_files=MAX_LOG_FILES, 
    max_size_mb=MAX_LOG_FOLDER_SIZE_MB
):
  """
  Manages the number and total size of files in a directory, deleting the oldest
  file when limits are exceeded.

  Args:
      directory_path (str): The path to the directory to manage.
      max_files (int, optional): The maximum number of files to keep. Defaults to 10.
      max_size_mb (int, optional): The maximum total size (in MB) of the directory. Defaults to 100.
  """
  # Get a list of files sorted by their modification time (oldest first)
  log_path = os.path.join(directory_path, f)
  files = [
    (os.path.getmtime(log_path), Path(f)) 
    for f in os.listdir(directory_path) if os.path.isfile()
  ]
  files.sort()

  # Calculate total size of all files
  total_size = sum(f.stat().st_size for f in (p for _, p in files))

  # Check if either limit is exceeded
  if len(files) > max_files or total_size > max_size_mb * 1024 * 1024:
    # Delete files until both limits are met (or list is empty)
    while len(files) > max_files or total_size > max_size_mb * 1024 * 1024:
      oldest_file, _ = files.pop(0)
      oldest_file.unlink()
      total_size -= oldest_file.stat().st_size
