from exercise.load import prep
import pandas as pd
import numpy as np

def test_drop_na():
    df = pd.DataFrame({'A': [1, 2, np.nan], 'B': [4, np.nan, 6], 'C': [7, 8, 9]})
    actual = prep.drop_na(df)

    expected = pd.DataFrame({'A': [1], 'B': [4], 'C': [7]})

    assert actual == expected


def test_read_dataframe():
    actual = prep.read_dataframe('test.csv')
    expected = pd.DataFrame({
    'A': {0: 1, 1: 5, 2: 9},
    'B': {0: 2, 1: 6, 2: 10},
    'C': {0: 3, 1: 7, 2: 11},
    'D': {0: 4, 1: 8, 2: 12}
    })
    
    assert actual == expected