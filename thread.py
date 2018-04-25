"""
Email Thread class
"""

from collections import OrderedDict
import webbrowser
from networkx.drawing.nx_agraph import graphviz_layout
import networkx as nx

import matplotlib.pyplot as plt
import numpy as nmp
import pandas as pd

from tools import nth_elt, h_index, save_fig

class Thread(object):

    """Email Thread"""

    cols = ['thread', 'subject', 'emails', 'users', 'start', 'days',
            'depth',
            'star_nodes',
            'h_index',
            'deg_max', 'deg_max_2', 'deg_max_3', 'deg_max_4', 'deg_max_5'
            ]

    def __init__(self, data):
        self.emails = data

        self.tree = nx.DiGraph()
        self.network = nx.DiGraph()

        self._build_tree(data)
        self._build_network(data)

        self.data = self._build_data()

    def _build_tree(self, data):
        """Build tree Graph object from email data

        :data: panda dataframe
        """
        for row in data[['msg_id', 'from_email']].itertuples():
            self.tree.add_node(row.msg_id, author=row.from_email)

        edges = data[['msg_id', 'in_reply_to']].dropna().values.tolist()
        self.tree.add_edges_from(edges)

    def _build_network(self, data):
        """Build network Graph object from email data

        :data: panda dataframe
        """

        # Put every pair of from/to on a single line by splitting to with ;
        data = data[['from_email', 'to_email']].dropna()
        edges = pd.DataFrame(data.to_email.str.split(';').tolist(), index=data.from_email).stack()

        # Extract, rename and reorder columns
        edges = edges.reset_index()[[0, 'from_email']]
        edges.columns = ['to_email', 'from_email']
        edges = edges[['from_email', 'to_email']]

        if edges.empty:
            return

        # Remove all edges addressed to mailing list (first message)
        edges = edges[edges.to_email != 'git@vger.kernel.org']

        # If the thread consists of one sender only, there's no network to build
        if edges.empty:
            return

        # Put each unique edge on its own line, with its frequence in 'weight'
        edges = edges.groupby(['from_email', 'to_email']).size().reset_index(name='weight')

        # Make it a relative weight (from 0 to 1) rather than a frequence
        edges['weight'] = edges['weight']/max(edges.weight)

        # Add edges
        for edge in edges.itertuples():
            self.network.add_edge(edge.from_email, edge.to_email, weight=edge.weight)

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
        degrees.sort(reverse=True)

        users = len(self.network.nodes) if self.network.nodes else 1

        row = [
            self.emails['thread'].tolist()[0],
            self.emails.loc[self.emails.date == min(self.emails.date), 'subject'].values[0],
            self.emails.shape[0], # Nb of emails
            users,
            min(self.emails.date),
            (max(self.emails.date) - min(self.emails.date)).days,
            nx.dag_longest_path_length(self.tree), # Depth
            sum(d > 1 for d in degrees), # Star nodes
            h_index(degrees),
            nth_elt(degrees, 0), nth_elt(degrees, 1), nth_elt(degrees, 2), nth_elt(degrees, 3), nth_elt(degrees, 4)
        ]

        result = OrderedDict(zip(self.cols, row))

        return result

    def draw_tree(self, show=True, save=False):
        """Display simple drawing of thread tree graph"""

        fig = plt.figure()
        ax = fig.add_subplot(111)

        pos = graphviz_layout(self.tree, prog='dot')

        # Colors
        cmap = plt.get_cmap('jet')
        author_seq = nx.get_node_attributes(self.tree, 'author').values()
        color = cmap(nmp.linspace(0, 1, len(author_seq)))
        color_d = dict(zip(author_seq, color))
        color_seq = [color_d[n] for n in author_seq]

        nx.draw(self.tree, pos, node_color=color_seq, ax=ax)

        if save:
            show = False
            save_fig(fig, 'img', 'tree', self.data['thread'])

        if show:
            plt.show(ax)

        plt.close(fig)

    def draw_network(self, show=True, save=False):
        """Display simple drawing of thread network graph"""

        fig = plt.figure()
        ax = fig.add_subplot(111)

        pos = nx.spring_layout(self.network)

        nx.draw_networkx_nodes(self.network, pos, ax=ax)
        weights = nx.get_edge_attributes(self.network, 'weight').values()

        for weight_dec in [0.5, 1]:
            edges_dec = [(u, v) for (u, v, d) in self.network.edges(data=True) if weight_dec-0.5 < d['weight'] <= weight_dec]
            nx.draw_networkx_edges(self.network, pos, edgelist=edges_dec,
                                   width=weight_dec*2, ax=ax)

        nx.draw_networkx_labels(self.network, pos, ax=ax)

        ax.axis('off')

        if save:
            show = False
            save_fig(fig, 'img', 'network', self.data['thread'])

        if show:
            plt.show(ax)

        plt.close(fig)

    def graph_info(self):
        """Print tree info"""
        print(nx.info(self.tree))

    def graph_network(self):
        """Print network info"""
        print(nx.info(self.network))

    def open(self, url='https://public-inbox.org/git/'):
        """Open thread in web browser"""
        webbrowser.open(url + self.emails['thread'].tolist()[0])
