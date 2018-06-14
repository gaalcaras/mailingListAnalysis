"""
Explore how basic thread categories interact with other thread variables.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

threads = pd.read_csv('data/working/threads_labeled.csv',
                      parse_dates=['start'],
                      infer_datetime_format=True)

# Which categories are mainly: patches, long discussions, big discussions?
var_cross = ['emails', 'users', 'days', 'patch']
agg_form = {}

for var in var_cross:
    agg_form[var] = ['mean', 'std']

threads_bycat = threads.groupby('category', as_index=False)
results = threads_bycat.agg(agg_form)
print(results)

#  for var in var_cross:
#      ax = sns.boxplot(x='category', y=var,
#                       data=threads[['category', var]], palette='Set3')
#      plt.show(ax)

threads['year'] = threads.start.dt.year
t = threads.pivot_table(index='year', columns='category', values='deg_max', aggfunc='count')
print(t)
