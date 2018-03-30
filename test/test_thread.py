"""
Tests for Thread class
"""

from thread import Thread
import pandas

THREAD1_DATA = pandas.read_csv('data/test_thread1.csv',
                               parse_dates=['date'],
                               infer_datetime_format=True)
THREAD1 = Thread(THREAD1_DATA)

THREAD2_DATA = pandas.read_csv('data/test_thread2.csv',
                               parse_dates=['date'],
                               infer_datetime_format=True)
THREAD2 = Thread(THREAD2_DATA)


class TestGraphData(object):
    def test_thread1(self):
        assert dict(THREAD1.data) == {
            'authors': 2,
            'depth': 4,
            'in_degree': 0.8,
            'star_nodes': 0,
            'duration': pandas.Timedelta(days=4, hours=10, minutes=58, seconds=26),
            'emails': 4,
            'thread': 149519831100002,
        }

    def test_thread2(self):
        assert dict(THREAD2.data) == {
            'authors': 4,
            'depth': 7,
            'in_degree': 0.93,
            'duration': pandas.Timedelta(days=12, hours=22, minutes=43, seconds=57),
            'star_nodes': 3,
            'emails': 15,
            'thread': 111896264700001,
        }
