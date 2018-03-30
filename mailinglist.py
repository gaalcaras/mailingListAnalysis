"""
Mailing List
"""

from thread import Thread
from tqdm import tqdm
import pandas as pd

def follow_thread(emails, first_msg_id):
    """Follow email replies to rebuild threads

    :emails: dict (key: msg_id, value: reply_to)
    :msg_id: first email msg_id

    :returns: dict (key: msg_id, value: first_msg_id)
    """

    thread_ids = [first_msg_id]

    def look_for_answers(msg_id):
        "Look recursively for emails that reply to msg_id"

        answers = [k for k, v in emails.items() if v in msg_id]

        if not answers:
            return

        thread_ids.extend(answers)
        look_for_answers(answers)

    look_for_answers([first_msg_id])

    return dict(map(lambda e: (e, first_msg_id), thread_ids))

class MailingList(object):

    """Emails"""

    def __init__(self, filepath):
        self.emails = pd.read_csv(filepath,
                                  parse_dates=['date'],
                                  infer_datetime_format=True)
        self.threads = pd.DataFrame()
        self._threads = dict()

    def make_threads(self):
        """Recognize threads in the mailing list by following replies, and adds
        a new 'thread' column that contains the Message-ID of the first message
        in the thread.
        """

        emails = self.emails[['msg_id', 'in_reply_to']]
        ids = pd.Series(emails.in_reply_to.values, index=emails.msg_id).to_dict()

        # Get first messages (no In-Reply-To header)
        first_msg_ids = [k for k, v in ids.items() if not isinstance(v, str)]

        thread = dict() # Key: Message-Id, Value: Thread-ID (first thread message ID)

        for msg_id in tqdm(first_msg_ids, desc='Reconstructing threads'):
            thread.update(follow_thread(ids, msg_id))

        self.emails['thread'] = self.emails.msg_id.map(thread)

    def process_threads(self):
        "Process each thread as a Thread object"

        thread_ids = self.emails.thread.dropna().unique()
        thread_df = pd.DataFrame(index=range(0, len(thread_ids)),
                                 columns=Thread.cols)

        for i, thread_id in tqdm(enumerate(thread_ids), desc='Processing threads'):
            thread_emails = self.emails[self.emails.thread == thread_id]
            thread = Thread(thread_emails)

            thread_df.loc[i] = [v for v in thread.data.values()]
            self._threads[str(thread_id)] = thread

        thread_df = thread_df.sort_values(by=['emails', 'authors'],
                                          ascending=[False, False])
        self.threads = thread_df

    def thread(self, thread_id):
        "Get thread with thread_id"
        return self._threads[thread_id]
