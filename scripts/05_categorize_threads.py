"""
Categorize threads.
"""

import pandas as pd
from categorize import categorize_threads

threads = pd.read_csv('data/working/threads2017.csv')
threads = categorize_threads(threads)

cat_count = threads.groupby('category').size().reset_index(name='count')
cat_count = cat_count.sort_values(by = 'count', ascending=False)

print(cat_count)
