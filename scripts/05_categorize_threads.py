"""
Categorize threads
"""

import pandas as pd
from categorize import categorize_threads

def build_categories(filepath):
    """Compute categories, print tally and return labeled threads"""
    threads = pd.read_csv(filepath)
    threads = categorize_threads(threads)

    cat_count = threads.groupby('category').size().reset_index(name='count')
    cat_count = cat_count.sort_values(by = 'count', ascending=False)
    cat_count['%']  = cat_count['count']*100/cat_count['count'].sum()

    email_count = threads.groupby('category').emails.sum().reset_index(name='email_count')
    email_count['emails_%']  = email_count['email_count']*100/email_count['email_count'].sum()

    result = pd.merge(cat_count, email_count, on='category')
    print(result)

    return threads

threads2017 = build_categories('data/working/threads2017.csv')
threads2017.to_csv('data/working/threads2017_labeled.csv', index=False)

threads = build_categories('data/working/threads.csv')
threads.to_csv('data/working/threads_labeled.csv', index=False)
