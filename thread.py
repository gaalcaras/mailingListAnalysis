"""
Email Thread class
"""

import networkx as nx
import numpy as nmp
import pandas as pd

class Thread(object):

    """Email Thread"""

    def __init__(self, data):
        self.emails = data

        self.graph = nx.DiGraph()
        self._build_graph(data)

        self.data = self._build_data()

    def _build_graph(self, data):
        """Build Graph object from email data

        :data: panda dataframe
        """
        self.graph.add_nodes_from(data.msg.unique())

        edges = data[['msg', 'reply_to']].dropna().values.tolist()
        self.graph.add_edges_from(edges)

    def data_frame(self):
        """
        Return thread data as pandas dataframe
        """
        return pd.DataFrame(data=self.data, index=[0])

    def _build_data(self):
        """
        Return thread data as dictionary
        """
        degrees = [d for n, d in self.graph.in_degree]
        result = {
            'depth': nx.dag_longest_path_length(self.graph),
            'in_degree': nmp.mean(degrees),
            'star_nodes': sum(d > 1 for d in degrees)
        }
        return result

    def graph_info(self):
        """Print graph info"""
        print(nx.info(self.graph))
