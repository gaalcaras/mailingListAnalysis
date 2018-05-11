import pandas as pd
from plot import scatter

threads = pd.read_csv('data/working/threads2017.csv')

def test_scatter():
    scatter(threads, ['emails', 'users'], show=False)
    scatter(threads, ['emails', 'users'], log=False, show=False)
