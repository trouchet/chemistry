import re


def convert_requirements_to_poetry(filename):
    """
    Converts packages from a requirements file to a string for Poetry.

    Args:
        filename (str): Path to the requirements file.

    Returns:
        str: A string containing package names and optional version specifications
            formatted for the [tool.poetry.dependencies] section in pyproject.toml.
    """
    dependencies_string = ""
    with open(filename, "r") as file:
        for line in file:
            # Remove comments and leading/trailing whitespaces
            package_line = line.strip().split("#")[0]
            if not package_line:
                continue

            # Extract package name and version (allow various formats)
            match = re.match(
                r"(?P<package_name>\w+(?:\-\w+)*)(?:\s*(?P<operator>==|<=|>=|<|>|!=)?\s*(?P<version>.*))?$",
                package_line,
            )
            if match:
                package_name = match.group("package_name")
                version = (
                    match.group("version") or "~"
                )  # Default to tilde (~) for any version
                dependencies_string += f'{package_name} = {{ version = "{version}" }}\n'
    return dependencies_string


# Example usage
requirements_file = "requirements.txt"
poetry_dependencies_string = convert_requirements_to_poetry(requirements_file)

print(poetry_dependencies_string)
