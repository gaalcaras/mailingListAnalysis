"""
Email Thread class
"""

from networkx.drawing.nx_agraph import graphviz_layout
import networkx as nx

import matplotlib.pyplot as plt
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
        for index, row in data[['msg', 'sender_name']].iterrows():
            self.graph.add_node(row.msg,
                                author=row.sender_name)

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
            'authors': len(self.emails.sender_name.unique()),
            'depth': nx.dag_longest_path_length(self.graph),
            'in_degree': nmp.mean(degrees),
            'star_nodes': sum(d > 1 for d in degrees)
        }
        return result

    def draw(self):
        """Display simple drawing of thread graph"""

        plt.subplot(121)

        pos = graphviz_layout(self.graph, prog='dot')

        # Colors
        cmap = plt.get_cmap('viridis')
        color = cmap(nmp.linspace(0, 1, self.data['authors']))
        color_d = dict(zip(self.emails.sender_name.unique(), color))
        author_seq = nx.get_node_attributes(self.graph, 'author').values()
        color_seq = [color_d[n] for n in author_seq]

        nx.draw(self.graph, pos, node_color=color_seq)

        plt.show()

    def graph_info(self):
        """Print graph info"""
        print(nx.info(self.graph))
