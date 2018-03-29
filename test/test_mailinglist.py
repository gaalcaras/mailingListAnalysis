"""
Tests for MailingList class
"""

from mailinglist import MailingList
import pandas

ML1 = MailingList('data/test_thread2.csv')


class TestMakeThreads(object):
    """Test number of emails tagged with correct thread id"""

    def test_ml1(self):
        ML1.make_threads()
        assert len(ML1.emails[ML1.emails.thread == 'tnxy899zzu7.fsf@arm.com']) == 15


class TestProcessThreads(object):

    def test_ml1(self):
        ML1.process_threads()
        assert set(ML1._threads.keys()) == set(['tnxy899zzu7.fsf@arm.com'])
