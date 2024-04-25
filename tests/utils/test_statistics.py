from api.utils.statistics import get_list_statistics, print_list_statistics


def test_get_list_statistics(sample_list):
    expected_stats = {
        "min": 1,
        "25%": 3.25,
        "50%": 5.5,
        "75%": 7.75,
        "90%": 9.1,
        "95%": 9.55,
        "99%": 9.91,
        "max": 10,
        "mean": 5.5,
        "std": 2.87,
        "var": 8.25,
        "skewness": 0.0,
        "kurtosis": -1.2,
        "iqr": 4.5,
        "mad": 2.5,
        "cv": 52.22,
        "entropy": 1.61,
    }

    stats = get_list_statistics(sample_list, precision=2)
    for descrip, value in expected_stats.items():
        assert stats[descrip] == value


def test_print_list_statistics(sample_list, capsys):
    print_list_statistics(sample_list)
    captured = capsys.readouterr()
    expected_output = """min      : 1
25%      : 3.25
50%      : 5.5
75%      : 7.75
90%      : 9.1
95%      : 9.55
99%      : 9.91
max      : 10
mean     : 5.5
std      : 2.87
var      : 8.25
skewness : 0.0
kurtosis : -1.2
iqr      : 4.5
mad      : 2.5
cv       : 52.22
entropy  : 1.61
"""
    assert captured.out == expected_output
