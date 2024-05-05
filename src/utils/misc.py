import re


def snake2camel(snake: str, start_lower: bool = False) -> str:
    """
    Converts a snake_case string to camelCase.
    Source: https://github.com/dmontagu/fastapi-utils

    Args:
        snake (str): snake_case string to convert.
        start_lower (bool): Whether to start the output string in lowercase.

    Returns:
        str: camelCase string equivalent to the input snake_case string.
    """
    camel = snake.title()
    camel = re.sub("([0-9A-Za-z])_(?=[0-9A-Z])", lambda m: m.group(1), camel)
    if start_lower:
        camel = re.sub("(^_*[A-Z])", lambda m: m.group(1).lower(), camel)
    return camel
