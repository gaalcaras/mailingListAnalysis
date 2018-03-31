"""
Email Thread class
"""

from collections import OrderedDict
from networkx.drawing.nx_agraph import graphviz_layout
import networkx as nx

import matplotlib.pyplot as plt
import numpy as nmp
import pandas as pd
import webbrowser

class Thread(object):

    """Email Thread"""

    cols = ['thread', 'emails', 'authors', 'duration', 'depth', 'in_degree', 'star_nodes']

    def __init__(self, data):
        self.emails = data

        self.graph = nx.DiGraph()
        self._build_graph(data)

        self.data = self._build_data()

    def _build_graph(self, data):
        """Build Graph object from email data

        :data: panda dataframe
        """
        for row in data[['msg_id', 'from_email']].itertuples():
            self.graph.add_node(row.msg_id,
                                author=row.from_email)

        edges = data[['msg_id', 'in_reply_to']].dropna().values.tolist()
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
        row = [
            self.emails['thread'].tolist()[0],
            self.emails.shape[0],
            len(self.emails.from_email.unique()),
            max(self.emails.date) - min(self.emails.date),
            nx.dag_longest_path_length(self.graph),
            round(nmp.mean(degrees), 2),
            sum(d > 1 for d in degrees)
        ]
        result = OrderedDict(zip(self.cols, row))
        return result

    def draw(self):
        """Display simple drawing of thread graph"""

        plt.subplot(121)

        pos = graphviz_layout(self.graph, prog='dot')

        # Colors
        cmap = plt.get_cmap('viridis')
        color = cmap(nmp.linspace(0, 1, self.data['authors']))
        color_d = dict(zip(self.emails.from_email.unique(), color))
        author_seq = nx.get_node_attributes(self.graph, 'author').values()
        color_seq = [color_d[n] for n in author_seq]

        nx.draw(self.graph, pos, node_color=color_seq)

        plt.show()

    def graph_info(self):
        """Print graph info"""
        print(nx.info(self.graph))

    def open(self):
        """Open thread in web browser"""
        webbrowser.open('https://public-inbox.org/git/' + self.emails['thread'].tolist()[0])
