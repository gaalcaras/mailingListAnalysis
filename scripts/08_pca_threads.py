"""
Perform PCA on threads in each year.
"""

import pandas as pd
import numpy as np
from pca import ThreadPCA
from categorize import categorize_threads

threads = pd.read_csv('data/working/threads.csv',
                      parse_dates=['start'],
                      infer_datetime_format=True)

# Compute a ratio
threads['ratio'] = np.log1p(threads['depth']) / np.log1p(threads['emails'])

# Remove trivial threads with no depth (they're basically one email threads)
threads = threads[threads.depth > 0]
threads = categorize_threads(threads)

years = sorted(threads.start.dt.year.unique())

for year in years:
    threads_year = threads.loc[threads.start.dt.year == year]
    pca = ThreadPCA(threads_year, ['star_nodes', 'ratio', 'deg_max', 'h_index', 'deg_max_2'])
    pca.to_imgs(year, scatter_color='category')
    pca.to_html(year)
