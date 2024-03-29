from numpy import histogram, quantile
from typing import List, Union
import plotly.express as px
import pandas as pd

from utils.constants import PLOT_CONFIDENCE

def plot_histogram(
    lst: list, 
    title_: str, 
    x_label: str, 
    bin_count: int = None
):
    if bin_count is None:
        bin_count = min(len(lst), 30)  # Assuming MIN_BIN_COUNT is 30

    # Compute the histogram
    hist, bins = histogram(lst, bins=bin_count, density=True)

    # Compute the bin values
    bin_values = [(bins[i] + bins[i+1]) / 2 for i in range(len(hist))]

    # Create a DataFrame for the histogram data
    hist_df = pd.DataFrame({'bin': bin_values, 'count': hist})

    # Create an interactive histogram plot using Plotly Express
    fig = px.bar(hist_df, x='bin', y='count', labels={'bin': x_label, 'count': 'Frequency'}, title=title_)
    fig.show()

def quantile_(lst: list, perc: float, digits: int = 2):
    return round(quantile(lst, perc), digits)
    
def print_list_statistics(lst: Union[List[int], List[float]]) -> None:
    print(f'min    : {min(lst)}')
    print(f'25%    : {quantile_(lst, 0.25)}')
    print(f'50%    : {quantile_(lst, 0.5)}')
    print(f'75%    : {quantile_(lst, 0.75)}')
    print(f'90%    : {quantile_(lst, 0.90)}')
    print(f'95%    : {quantile_(lst, 0.95)}')
    print(f'99%    : {quantile_(lst, 0.99)}')
    print(f'max    : {max(lst)}')

def plot_confidence_histogram(
    lst: list,
    title_: str,
    x_label: str, 
    bin_count: int,
    is_verbose: bool = False
):
    if(is_verbose):
        print_list_statistics(lst)
    
    # Calculate the 99th percentile
    percentile_confidence = quantile(lst, PLOT_CONFIDENCE)
    
    # Filter out counts greater than the 99th percentile
    filtered_list = [
        count 
        for count in lst 
        if count <= percentile_confidence
    ]
    
    plot_histogram(filtered_list, title_, x_label, bin_count)