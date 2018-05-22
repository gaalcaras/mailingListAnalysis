"""
Generate an HTML grid of tree graphs from the 2017 threads.
"""

import pandas as pd
import numpy as np
from gridgraph import gridgraph

threads = pd.read_csv('data/working/threads2017.csv')

# Add new metrics to refine typology
threads['deg_delta'] = round((np.log1p(threads['deg_max']) / np.log1p(threads['emails'])), 2)
threads['star_nodes_i'] = round((np.log1p(threads['star_nodes']) / np.log1p(threads['emails'])), 2)

# Keep only threads containing 10 emails
threads_e10 = threads[threads.emails == 10]
threads_h3 = threads[threads.h_index == 3]

# Build the grid of graphs
gridgraph(threads_e10, 'output/gridgraph_17_e10.html')
gridgraph(threads_h3, 'output/gridgraph_17_h3.html')
