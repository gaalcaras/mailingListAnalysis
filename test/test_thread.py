import pandas
from thread import Thread

thread1_data = pandas.read_csv('data/test_thread1.csv')
thread1 = Thread(thread1_data)

def test_graph_data():
    assert dict(thread1.data) == {
        'authors': 2,
        'depth': 4,
        'in_degree': 0.8,
        'star_nodes': 0,
        'emails': 4,
        'thread': 149519831100002,
    }
