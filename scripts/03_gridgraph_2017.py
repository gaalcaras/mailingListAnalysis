"""
Generate an HTML grid of tree graphs from the 2017 threads.
"""

import pandas as pd
import numpy as np
from gridgraph import gridgraph

threads = pd.read_csv('data/working/threads2017_labeled.csv')

# Add new metrics to refine typology
threads['deg_delta'] = round((np.log1p(threads['deg_max']) / np.log1p(threads['emails'])), 2)
threads['deg_ratio'] = round((np.log1p(threads['deg_max_2']) / np.log1p(threads['deg_max'])**2), 2)
threads['star_nodes_i'] = round((np.log1p(threads['star_nodes']) / np.log1p(threads['emails'])), 2)

# Keep only threads containing 10 emails
threads_e10 = threads[threads.emails == 10]
threads_h3 = threads[threads.h_index == 3]

# Build the grid of graphs
gridgraph(threads_e10, '2017_emails10')
gridgraph(threads_h3, '2017_h_index_3')

for category in threads.category.unique():
    threads_subset = threads[threads.category == category]
    gridgraph(threads_subset, '2017_{}'.format(category))
