from typing import List, Union
import pandas as pd

from scipy.stats import entropy
import numpy as np

NumberList = Union[List[int], List[float]]

def get_list_statistics(lst: NumberList, precision: int = 2) -> dict:
    from numpy import percentile, mean, std, abs, var

    mean_value = mean(lst)
    std_value = std(lst)
    cv_value = (std_value / mean_value) * 100 if mean_value != 0 else np.nan

    stats = {
        "min": min(lst),
        "25%": percentile(lst, 25),
        "50%": percentile(lst, 50),
        "75%": percentile(lst, 75),
        "90%": percentile(lst, 90),
        "95%": percentile(lst, 95),
        "99%": percentile(lst, 99),
        "max": max(lst),
        "mean": mean_value,
        "std": std_value,
        "var": var(lst),
        "skewness": pd.Series(lst).skew(),
        "kurtosis": pd.Series(lst).kurtosis(),
        "iqr": percentile(lst, 75) - np.percentile(lst, 25),
        "mad": mean(abs(lst - mean(lst))),
        "cv": cv_value,
        "entropy": entropy(np.histogram(lst, bins='auto')[0]),
    }

    return {
        descrip: round(value, precision) 
        for descrip, value in stats.items()
    }


def print_list_statistics(lst: Union[List[int], List[float]]) -> None:
    stats = get_list_statistics(lst)
    max_len = max(len(descrip) for descrip, _ in stats.items())

    for descrip, value in stats.items():
        print(f'{descrip.ljust(max_len)} : {value}')
