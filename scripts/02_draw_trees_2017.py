"""
Draw tree graphs from the 2017 threads and save them.
It can take some time, so you probably only need to run it once.
"""

import pandas as pd
from mailinglist import MailingList
from gridgraph import gridgraph, draw_trees

# Load emails from year 2017
emails2017 = MailingList('data/working/year2017_threaded.csv')

# Process threads (trees + networks)
emails2017.process_threads()

# Let's go!
draw_trees(emails2017, emails2017.threads.thread)
