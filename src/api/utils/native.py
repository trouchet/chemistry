import pickle
import dill
import cloudpickle
from random import sample
from timy import timer
from secrets import choice
from string import ascii_letters, digits
from collections import defaultdict

from api.utils.constants import DEFAULT_TOKEN_LENGTH

def remove_duplicates_and_select_max(
    tuples_list: tuple
) -> list:
    # Convert the list of tuples into a dictionary
    tuples_dict = defaultdict(int)
    for string, number in tuples_list:
        tuples_dict[string] = max(tuples_dict[string], number)
    
    # Convert the dictionary back to a list of tuples
    result = [(string, number) for string, number in tuples_dict.items()]
    return result

def setify_list(lst: list) -> list:
    return list(set(lst))


def remove_list_from_list(list1, list2) -> list:
    return [x for x in list1 if x not in list2]


def get_random_element(arr: list) -> any:
    return sample(arr, 1)[0]


def generate_random_tokens(
    num_tokens: int = 1, token_length: int = DEFAULT_TOKEN_LENGTH
) -> list:
    """Generate random tokens.

    Args:
        num_tokens (int, optional): Number of tokens to generate. Defaults to 1.
        token_length (int, optional): Length of each token. Defaults to DEFAULT_TOKEN_LENGTH.

    Returns:
        list: List of generated tokens.

    Examples:
    >>> len(generate_random_tokens())
    1
    >>> len(generate_random_tokens(5))
    5
    >>> all(len(token) == DEFAULT_TOKEN_LENGTH for token in generate_random_tokens())
    True
    >>> all(len(token) == 10 for token in generate_random_tokens(5, 10))
    True
    """
    tokens = []
    for _ in range(num_tokens):
        token = ''.join(choice(ascii_letters + digits) for _ in range(token_length))
        tokens.append(token)

    return tokens


def invert_dict(dict_: dict) -> dict:
    new_dict = dict()

    # Validate input
    for value in dict_.values():
        if not isinstance(value, list):
            emsg = 'All values must be lists!'
            raise ValueError(emsg)

    for key, value in dict_.items():
        for el in value:
            new_dict_key = list(new_dict.keys())
            if el in new_dict_key:
                new_dict[el].append(key)
            else:
                new_dict[el] = [key]

    return new_dict


def flatten_list(lst: list) -> list:
    new_lst = []

    for el in lst:
        if isinstance(el, list):
            new_lst += flatten_list(el)
        else:
            new_lst.append(el)

    return new_lst


def sum_dicts(dict_list) -> dict:
    result = {}
    for d in dict_list:
        for key, value in d.items():
            if key not in result:
                result[key] = value
            else:
                result[key] += value
    return result


@timer()
def load_pickle(pkl_filepath: str) -> any:
    with open(pkl_filepath, 'rb') as f:
        return pickle.load(f)


@timer()
def dump_pickle(dump_file: any, pkl_filepath: str) -> None:
    # Dump training data to pickle
    with open(pkl_filepath, 'wb') as f:
        pickle.dump(dump_file, f)


@timer()
def load_dill(dill_filepath: str) -> None:
    with open(dill_filepath, 'rb') as f:
        return dill.load(f)


@timer()
def dump_dill(dump_file: any, dill_filepath: str) -> None:
    # Dump training data to dill
    with open(dill_filepath, 'wb') as f:
        dill.dump(dump_file, f)


@timer()
def load_cloudpickle(pkl_filepath: str) -> None:
    with open(pkl_filepath, 'rb') as f:
        return cloudpickle.load(f)


@timer()
def dump_cloudpickle(dump_file: any, pkl_filepath: str) -> None:
    # Dump training data to cloudpickle
    with open(pkl_filepath, 'wb') as f:
        cloudpickle.dump(dump_file, f)
