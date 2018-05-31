"""
Load all email data, then process threads and export updated datasets.
"""

import pandas as pd
from mailinglist import MailingList

# Load the mailing list data
emails = MailingList('data/raw/2017_03_30_git_emails.csv')

# Build and process threads
emails.make_threads()
emails.process_threads()

# Export emails and threads
emails.emails.to_csv('data/working/emails_threaded.csv', index=False)
emails.threads.to_csv('data/working/threads.csv', index=False)
