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

def test_thread_data():
    assert dict(THREAD1.data) == {
        'authors': 3,
        'depth': 4,
        'in_degree': 0.8,
        'star_nodes': 0,
        'duration': pandas.Timedelta(days=4, hours=10, minutes=58, seconds=26),
        'emails': 4,
        'thread': 149519831100002,
    }

    assert dict(THREAD2.data) == {
        'authors': 5,
        'depth': 7,
        'in_degree': 0.93,
        'duration': pandas.Timedelta(days=12, hours=22, minutes=43, seconds=57),
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
