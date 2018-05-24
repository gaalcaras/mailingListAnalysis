"""
Explore how basic thread categories interact with other thread variables.
"""

import pandas as pd

threads = pd.read_csv('data/working/threads2017_labeled.csv')

# Which categories are mainly: patches, long discussions, big discussions?
var_cross = ['emails', 'users', 'days', 'patch']
agg_form = {}

for var in var_cross:
    agg_form[var] = ['mean', 'std']

threads_bycat = threads.groupby('category', as_index=False)
results = threads_bycat.agg(agg_form)
print(results)
