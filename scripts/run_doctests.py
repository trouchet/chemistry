import os
import sys
import doctest
from doctest import DocTest
from typing import List


def find_python_files(directory):
    """
    Find all Python files in the given directory (and its subdirectories).

    Args:
        directory (str): The directory to search in.

    Returns:
        list: List of file paths.
    """
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def gather_doctests(files: List[str]) -> List[DocTest]:
    """
    Gather all doctests from the given list of Python files.

    Args:
        files (list): List of file paths.

    Returns:
        list: List of doctests as DocTest objects.
    """
    doctests = []
    parser = doctest.DocTestParser()
    for file in files:
        try:
            with open(file, "r") as f:
                code = f.read()
                test = parser.get_doctest(code, {}, file, file, 0)
                if test.examples:
                    doctests.append(test)
                else:
                    pass
        except Exception as e:
            print(f"** Error reading {file}: {e} **")
    return doctests


def run_tests(doctests: List[DocTest]) -> None:
    globs = {}
    for test in doctests:
        try:
            doctest.run_docstring_examples(test.examples, globs, test.filename)
        except Exception as e:  # Catch unexpected exceptions
            print(f"** Unexpected error: {e} - {test.filename} **")


if __name__ == "__main__":
    # Get the root directory from command line argument, defaulting to current working directory
    root_directory = sys.argv[1] if len(sys.argv) > 1 else "."

    # Find all Python files in the specified root directory
    files = find_python_files(root_directory)

    # Gather all doctests from the files
    doctests = gather_doctests(files)

    # Run the collected doctests
    run_tests(doctests)
