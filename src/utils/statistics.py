from typing import List, Union
import pandas as pd

from scipy.stats import entropy
import numpy as np

NumberList = Union[List[int], List[float]]

def get_list_statistics(lst: NumberList, precision: int = 2) -> dict:
    """
    Calcula estatísticas descritivas de uma lista numérica.

    Parâmetros:
    - lst (NumberList): A lista numérica para a qual as estatísticas serão calculadas.
    - precision (int): O número de casas decimais para arredondamento (padrão é 2).

    Retorna:
    - dict: Um dicionário contendo as estatísticas descritivas calculadas, com as chaves representando
            os nomes das estatísticas e os valores representando os valores calculados.

    Exemplo:
    >>> get_list_statistics([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    {'min': 1, '25%': 3.25, '50%': 5.5, '75%': 7.75, '90%': 9.1, '95%': 9.55, '99%': 9.91, 'max': 10, 'mean': 5.5, 'std': 3.03, 'var': 9.2, 'skewness': 0.0, 'kurtosis': -1.22, 'iqr': 4.5, 'mad': 2.5, 'cv': 55.09, 'entropy': 2.302585092994046}
    """
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
    """
    Imprime as estatísticas descritivas de uma lista numérica formatada.

    Parâmetros:
    - lst (Union[List[int], List[float]]): A lista numérica para a qual as estatísticas serão calculadas e impressas.

    Retorna:
    - None

    Exemplo:
    >>> print_list_statistics([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    min       : 1
    25%       : 3.25
    50%       : 5.5
    75%       : 7.75
    90%       : 9.1
    95%       : 9.55
    99%       : 9.91
    max       : 10
    mean      : 5.5
    std       : 3.03
    var       : 9.2
    skewness  : 0.0
    kurtosis  : -1.22
    iqr       : 4.5
    mad       : 2.5
    cv        : 55.09
    entropy   : 2.302585092994046
    """
    stats = get_list_statistics(lst)
    max_len = max(len(descrip) for descrip, _ in stats.items())

    for descrip, value in stats.items():
        print(f'{descrip.ljust(max_len)} : {value}')
