from re import search
from src.api.utils.constants import MIN_LENGTH

def is_password_strong_dict(password: str) -> bool:
    """
    Checks if a password meets minimum security requirements.

    Args:
        password (str): The password to be checked.

    Returns:
        dict: A dictionary with the requirements and whether they are met.
    """
    
    has_lowercase = search(r"[a-z]", password)
    has_uppercase = search(r"[A-Z]", password)
    has_number = search(r"\d", password)
    has_special_char = search(r"[^\w\s]", password)

    return {
        "min_length": len(password) >= MIN_LENGTH,
        "has_lowercase": bool(has_lowercase),
        "has_uppercase": bool(has_uppercase),
        "has_number": bool(has_number),
        "has_special_char": bool(has_special_char)
    }

def is_password_strong(password: str) -> bool:
    """
    Checks if a password meets minimum security requirements.

    Args:
        password (str): The password to be checked.

    Returns:
        bool: True if the password is strong, False otherwise.
    """
    from functools import reduce 
    and_map = lambda x, y: x and y
    return reduce(and_map, is_password_strong_dict(password).values())
