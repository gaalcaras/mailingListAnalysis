"""
Mailing List
"""

from thread import Thread
import pandas as pd

def follow_thread(emails, first_msg_id):
    """Follow email replies to rebuild threads

    :emails: pandas dataframe
    :msg_id: first email msg_id

    :returns: list of msg ids of the thread
    """

    thread_ids = [first_msg_id]

    def look_for_answers(msg_id):
        "Look recursively for emails that reply to msg_id"

        answers = emails[emails.in_reply_to.isin(msg_id)].msg_id.tolist()

        if not answers:
            return

        thread_ids.extend(answers)
        look_for_answers(answers)

    look_for_answers([first_msg_id])

    return thread_ids

class MailingList(object):

    """Emails"""

    def __init__(self, filepath):
        self.emails = pd.read_csv(filepath, parse_dates=['date'])
        self.threads = pd.DataFrame()
        self._threads = dict()

    def make_threads(self):
        "Recognize threads in the mailing list"

        emails = self.emails[['date', 'msg_id', 'in_reply_to']]
        emails = emails.set_index(['date'])

        thread_start = emails[emails.in_reply_to.isnull()]

        for index, row in thread_start.iterrows():
            emails_target = emails.loc[index:]
            msg_id = row['msg_id']

            threads_ids = follow_thread(emails_target, msg_id)

            self.emails.loc[self.emails.msg_id.isin(threads_ids), 'thread'] = msg_id

    def process_threads(self):
        "Process each thread as a Thread object"

        thread_ids = self.emails.thread.unique()
        thread_df = pd.DataFrame(index=range(0, len(thread_ids)),
                                 columns=Thread.cols)

        for i, thread_id in enumerate(thread_ids):
            thread_emails = self.emails[self.emails.thread == thread_id]
            thread = Thread(thread_emails)

            thread_df.loc[i] = [v for v in thread.data.values()]
            self._threads[str(thread_id)] = thread

        self.threads = thread_df

    def thread(self, thread_id):
        "Get thread with thread_id"
        return self._threads[thread_id]
