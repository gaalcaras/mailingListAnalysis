"""
Perform PCA on 2017 threads.
"""

import pandas as pd
import numpy as np
from pca import ThreadPCA

threads = pd.read_csv('data/threads2017.csv')

# Compute a ratio
threads['ratio'] = np.log1p(threads['depth']) / np.log1p(threads['emails'])

# Remove trivial threads with no depth (they're basically one email threads)
threads = threads[threads.depth > 0]

# Perform pca
pca = ThreadPCA(threads, ['star_nodes', 'ratio', 'deg_max', 'h_index', 'deg_max_2'])

# Draw scree plot
pca.scree()

# Draw scatter plot (first two components), coloring threads with h_index
pca.scatter(color='h_index')

# Draw correlation circle (first two components)
pca.corr_circle()

# Let's get a closer look at some of these threads
pca.show_points({1: 1.7, 2: 5.9}) # All of them have deg_max_2 = 0
pca.show_points({1: 1.9, 2: 3.7}) # All of them have deg_max_2 = 1
pca.show_points({1: 5.1, 2: 0.7}, around=0.5)
