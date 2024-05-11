import pytest
from backend.app.api.utils.native import (
    invert_dict,
    flatten_list,
    sum_dicts,
    remove_list_from_list,
)


def test_invert_dict_failed(mangled_sample_dict):
    with pytest.raises(ValueError) as e:
        invert_dict(mangled_sample_dict)

    assert str(e.value) == "All values must be lists!"


def test_invert_dict(sample_dict):
    inverted_dict = invert_dict(sample_dict)
    assert inverted_dict == {
        1: ["a"],
        2: ["a", "b"],
        3: ["a", "c"],
        4: ["b"],
        6: ["b", "c"],
        9: ["c"],
    }


def test_flatten_list():
    lst = [[1, 2], [3, [4, 5]], 6]
    assert flatten_list(lst) == [1, 2, 3, 4, 5, 6]


def test_sum_dicts():
    dict_list = [{"a": 1, "b": 2}, {"b": 3, "c": 4}, {"c": 5, "d": 6}]
    assert sum_dicts(dict_list) == {"a": 1, "b": 5, "c": 9, "d": 6}


@pytest.mark.parametrize(
    "list1, list2, expected",
    [
        ([1, 2, 3, 4, 5], [2, 4], [1, 3, 5]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], []),
        ([1, 2, 3, 4, 5], [], [1, 2, 3, 4, 5]),
        ([], [1, 2, 3, 4, 5], []),
        ([], [], []),
    ],
)
def test_remove_list_from_list(list1, list2, expected):
    assert remove_list_from_list(list1, list2) == expected


def test_remove_list_from_list_handles_duplicates():
    list1 = [1, 2, 2, 3, 4, 5]
    list2 = [2, 4]
    expected = [1, 3, 5]
    assert remove_list_from_list(list1, list2) == expected


def test_remove_list_from_list_returns_new_list():
    list1 = [1, 2, 3, 4, 5]
    list2 = [2, 4]
    result = remove_list_from_list(list1, list2)
    assert result is not list1
    assert result is not list2
