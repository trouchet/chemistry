from backend.utils.security import is_password_strong


def test_empty_password():
    password = ""
    assert is_password_strong(password) == False


def test_weak_password_short():
    password = "short"

    assert is_password_strong(password) == False


def test_weak_password_no_lowercase():
    password = "PASSWORD123!"
    assert is_password_strong(password) == False


def test_weak_password_no_uppercase():
    password = "password123!"
    assert is_password_strong(password) == False


def test_weak_password_no_number():
    password = "PasswordStrong!"
    assert is_password_strong(password) == False


def test_weak_password_no_special_char():
    password = "Password1234"
    assert is_password_strong(password) == False


def test_strong_password():
    password = "StrongP@ssw0rd123"
    assert is_password_strong(password) == True
