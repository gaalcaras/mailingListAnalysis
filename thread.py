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

        self.tree = nx.DiGraph()

        self._build_tree(data)

        self.data = self._build_data()

    def _build_tree(self, data):
        """Build tree Graph object from email data

        :data: panda dataframe
        """
        for row in data[['msg_id', 'from_email']].itertuples():
            self.tree.add_node(row.msg_id,
                                author=row.from_email)

        edges = data[['msg_id', 'in_reply_to']].dropna().values.tolist()
        self.tree.add_edges_from(edges)

    def data_frame(self):
        """
        Return thread data as pandas dataframe
        """
        return pd.DataFrame(data=self.data, index=[0])

    def _build_data(self):
        """
        Return thread data as dictionary
        """
        degrees = [d for n, d in self.tree.in_degree]
        row = [
            self.emails['thread'].tolist()[0],
            self.emails.shape[0],
            len(self.emails.from_email.unique()),
            max(self.emails.date) - min(self.emails.date),
            nx.dag_longest_path_length(self.tree),
            round(nmp.mean(degrees), 2),
            sum(d > 1 for d in degrees)
        ]
        result = OrderedDict(zip(self.cols, row))
        return result

    def draw(self):
        """Display simple drawing of thread tree graph"""

        plt.subplot(121)

        pos = graphviz_layout(self.tree, prog='dot')

        # Colors
        cmap = plt.get_cmap('jet')
        color = cmap(nmp.linspace(0, 1, self.data['authors']))
        color_d = dict(zip(self.emails.from_email.unique(), color))
        author_seq = nx.get_node_attributes(self.tree, 'author').values()
        color_seq = [color_d[n] for n in author_seq]

        nx.draw(self.tree, pos, node_color=color_seq)

        plt.show()

    def graph_info(self):
        """Print tree info"""
        print(nx.info(self.tree))

    def open(self):
        """Open thread in web browser"""
        webbrowser.open('https://public-inbox.org/git/' + self.emails['thread'].tolist()[0])
