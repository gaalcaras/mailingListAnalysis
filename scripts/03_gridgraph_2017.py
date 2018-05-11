"""
Generate an HTML grid of tree graphs from the 2017 threads.
"""

import pandas as pd
from gridgraph import gridgraph

threads = pd.read_csv('data/working/threads2017.csv')

# Keep only threads containing 10 emails
threads10 = threads[threads.emails == 10]

# Build the grid of graphs
gridgraph(threads10, 'output/gridgraph_17_10.html')
