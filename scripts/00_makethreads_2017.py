"""
Load 2017 email data, then process threads and export updated datasets.
"""

import pandas as pd
from mailinglist import MailingList

# Load the mailing list data
emails2017 = MailingList('data/working/year2017_threaded.csv')

# Build and process threads
emails2017.make_threads()
emails2017.process_threads()

# Export emails and threads
emails2017.emails.to_csv('data/working/year2017_threaded.csv', index=False)
emails2017.threads.to_csv('data/working/threads2017.csv', index=False)

# Select a thread and draw its tree
emails2017.thread('20170213152011.12050-1-pclouds@gmail.com').draw_tree()

# Open the thread in your browser
emails2017.thread('20170213152011.12050-1-pclouds@gmail.com').open()
