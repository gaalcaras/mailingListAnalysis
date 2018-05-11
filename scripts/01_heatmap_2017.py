"""
Draw some heatmap to explore thread data
"""

import pandas as pd
import heatmap as ht

threads = pd.read_csv('data/working/threads2017.csv')

# Keep only threads containing 10 emails
threads10 = threads[threads.emails == 10]

# Draw some mosaics
ht.heatmap_count(threads10, ['h_index', 'star_nodes'])
ht.ordered_mosaic(threads10, ['star_nodes', 'depth'])
