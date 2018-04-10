"""
Tests for Thread class
"""

from thread import Thread
from mailinglist import MailingList
import pandas

THREAD1_DATA = pandas.read_csv('data/test_thread1.csv',
                               parse_dates=['date'],
                               infer_datetime_format=True)
THREAD1 = Thread(THREAD1_DATA)

THREAD2_DATA = pandas.read_csv('data/test_thread2.csv',
                               parse_dates=['date'],
                               infer_datetime_format=True)
THREAD2 = Thread(THREAD2_DATA)

ML1 = MailingList('data/test_sample1.csv')
ML1.make_threads()
ML1.process_threads()
THREAD3 = ML1.thread('20170520214233.7183-1-avarab@gmail.com')

def test_thread_data():
    assert dict(THREAD1.data) == {
        'users': 3,
        'depth': 4,
        'star_nodes': 0,
        'h_index': 1,
        'start': pandas.Timestamp('2017-05-19 12:48:34'),
        'duration': pandas.Timedelta(days=4, hours=10, minutes=58, seconds=26),
        'deg_max': 1,
        'deg_max_2': 1,
        'deg_max_3': 1,
        'deg_max_4': 1,
        'deg_max_5': 0,
        'emails': 4,
        'thread': 149519831100002,
    }

    assert dict(THREAD2.data) == {
        'users': 5,
        'depth': 7,
        'h_index': 2,
        'start': pandas.Timestamp('2005-06-16 22:44:32'),
        'duration': pandas.Timedelta(days=12, hours=22, minutes=43, seconds=57),
        'deg_max': 2,
        'deg_max_2': 2,
        'deg_max_3': 2,
        'deg_max_4': 1,
        'deg_max_5': 1,
        'star_nodes': 3,
        'emails': 15,
        'thread': 111896264700001,
    }

def test_network_data():
    assert len(THREAD1.network.nodes) == 3
    assert len(THREAD1.network.edges) == 4

    assert len(THREAD2.network.nodes) == 5
    assert len(THREAD2.network.edges) == 6

def test_tree_data():
    assert len(THREAD1.tree.nodes) == 5
    assert len(THREAD1.tree.edges) == 4

    assert len(THREAD2.tree.nodes) == 15
    assert len(THREAD2.tree.edges) == 14

def test_draw_tree():
    THREAD1.draw_tree(show=False)
    THREAD2.draw_tree(show=False)
    THREAD3.draw_tree(show=False)

def test_draw_network():
    THREAD1.draw_network(show=False)
    THREAD2.draw_network(show=False)
    THREAD3.draw_network(show=False)
