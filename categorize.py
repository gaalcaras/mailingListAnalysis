"""
Categorize threads.
"""

def categorize_threads(threads):
    """Add column 'category' with thread category.

    :threads: threads pandas dataframe
    """

    # The 'default' category: pretty even tree discussions
    threads.loc[:, 'category'] = 'tree'

    # Trivial threads with no depth (they're basically one email threads)
    threads.loc[threads.depth == 0, 'category'] = 'atom'

    # Combs (mainly patches)
    threads.loc[threads.deg_max_2 == 0, 'category'] = 'comb'

    # Comets (combs with a tail : mainly patches and some comments)
    threads.loc[threads.deg_max_2 == 1, 'category'] = 'comet'

    # Stringy (back and forth threads with no star_nodes)
    threads.loc[(threads.deg_max_2 == 1) & (threads.deg_max == 1), 'category'] = 'stringy'

    # Waterfall (huge patches)
    waterfall_cond = ((threads.h_index == 3) & (threads.deg_gini >= 0.7)) | (threads.h_index > 3)
    threads.loc[waterfall_cond, 'category'] = 'waterfall'

    return threads
