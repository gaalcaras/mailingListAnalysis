"""
Tests for Thread class
"""

from thread import Thread
import os
from mailinglist import MailingList
import pandas

THREAD1_DATA = pandas.read_csv('data/test/test_thread1.csv',
                               parse_dates=['date'],
                               infer_datetime_format=True)
THREAD1 = Thread(THREAD1_DATA)

THREAD2_DATA = pandas.read_csv('data/test/test_thread2.csv',
                               parse_dates=['date'],
                               infer_datetime_format=True)
THREAD2 = Thread(THREAD2_DATA)

THREAD3_DATA = pandas.read_csv('data/test/test_thread3.csv',
                               parse_dates=['date'],
                               infer_datetime_format=True)
THREAD3 = Thread(THREAD3_DATA)

ML1 = MailingList('data/test/test_sample1.csv')
ML1.make_threads()
ML1.process_threads()
THREAD4 = ML1.thread('20170520214233.7183-1-avarab@gmail.com')

def test_thread_data():
    assert dict(THREAD1.data) == {
        'users': 3,
        'depth': 4,
        'star_nodes': 0,
        'h_index': 1,
        'start': pandas.Timestamp('2017-05-19 12:48:34'),
        'subject': '[PATCH 01/15] handle_revision_arg: reset dotdot consistently',
        'patch': 1,
        'days': 4,
        'deg_gini': 0.2,
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
        'subject': 'Stacked GIT 0.1 (a.k.a. quilt for git)',
        'patch': 0,
        'days': 12,
        'deg_gini': 0.4,
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
    THREAD4.draw_tree(show=False)

    # Test save argument
    THREAD1.draw_tree(save=True)
    filepath = os.path.join('assets', 'img', 'tree', '149519831100002.svg')
    assert os.path.isfile(filepath) == True
    os.remove(filepath)

def test_draw_network():
    THREAD1.draw_network(show=False)
    THREAD2.draw_network(show=False)
    THREAD3.draw_network(show=False)
    THREAD4.draw_network(show=False)

    # Test save argument
    THREAD1.draw_network(save=True)
    filepath = os.path.join('assets', 'img', 'network', '149519831100002.svg')
    assert os.path.isfile(filepath) == True
    os.remove(filepath)
