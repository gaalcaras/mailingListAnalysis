"""
pca.py

Class to perform PCA and display helpful plots to help and explain the data.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.decomposition import PCA

def log_norm_transform(data):
    """Returns the data after applying log and standardization it."""
    result = np.log1p(data)
    scaler = StandardScaler()
    scaler.fit(result)
    return scaler.transform(result)


class ThreadPCA(object):

    def __init__(self, data, features, dimensions=3):
        """Perform PCA using

        :data: pandas dataframe
        :features: list of features used to perform PCA
        :dimensions: number of components returned
        """

        self.transformer = FunctionTransformer(log_norm_transform)
        self.data = data
        self.features = features
        self.data_t = self.transformer.transform(data[features])
        self.table = {}

        self.pca = PCA(dimensions)
        self.pca.fit(self.data_t)
        self.projected = self.pca.transform(self.data_t)

        self.match_data_transform()

    def scatter(self, components=(1, 2), color=None, show=True):
        """Draw a scatter plot of points along PC axes.

        :components: PC numbers to be used on the x and y axes
        :color: feature name to color points on the graph
        :show: display the graph
        """

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        # Center axis around (0,0)
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')

        # Keep ticks on bottom and left axis and make them protrude in both directions
        ax.xaxis.set_tick_params(bottom=True, top=False, direction='inout')
        ax.yaxis.set_tick_params(left=True, right=False, direction='inout')

        # Eliminate upper and right axes
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        if color:
            scatter = plt.scatter(self.projected[:, components[0]-1],
                                  self.projected[:, components[1]-1],
                                  alpha=0.5,
                                  c=self.data[color], edgecolor='none',
                                  cmap=plt.cm.get_cmap('Spectral',
                                                       len(self.data[color].unique())))

            # Add a colorbar
            cbar = plt.colorbar(scatter)

            # Label the colorbar and adjust its position
            cbar.ax.set_ylabel(color, rotation=90)
            cbar.ax.get_yaxis().labelpad = 15
        else:
            scatter = plt.scatter(self.projected[:, components[0]-1],
                                  self.projected[:, components[1]-1],
                                  alpha=0.5)

        ax.add_artist(scatter)

        # Get explained variances as percentage for each component
        exp_var_cp1 = round(self.pca.explained_variance_ratio_[components[0]-1]*100)
        exp_var_cp2 = round(self.pca.explained_variance_ratio_[components[1]-1]*100)

        # Label the axes with PC number and explained variance %
        ax.set_xlabel('PC {} ({}%)'.format(components[0], exp_var_cp1),
                      horizontalalignment='right', x=1)
        ax.set_ylabel('PC {} ({}%)'.format(components[1], exp_var_cp2),
                      verticalalignment='bottom', y=0.05)

        # Give the plot a title
        ax.set_title('PCA (PC{}xPC{})'.format(components[0], components[1]))

        if show:
            plt.show()

        plt.close(fig)

    def scree(self, show=True):
        """Draw PCA's scree plot"""

        # Create figure
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        # Draw barplot
        x = np.arange(len(self.pca.components_))
        plt.bar(x, self.pca.explained_variance_ratio_)

        # Add explained variance % on top of each bar
        for lab_x, lab_y in enumerate(self.pca.explained_variance_ratio_):
            ax.text(lab_x, lab_y+0.03,
                    str(round(lab_y, 2)),
                    horizontalalignment='center')

        # Change name of ticks
        plt.xticks(x, ('PC{}'.format(str(i+1)) for i in x))
        ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

        ax.set_title('Scree plot')

        if show:
            plt.show(fig)

        plt.close(fig)

    def corr_circle(self, components=(1, 2), show=True):
        """Draw a correlation circle.

        :components: PC numbers to be used on the x and y axis
        :show: display the graph
        """

        # Create figure
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        # Keep figure square
        ax.set_aspect('equal')

        # Center axis around (0,0)
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')

        # Eliminate upper and right axes
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        # Keep ticks on bottom and left axis and make them protrude in both directions
        ax.xaxis.set_tick_params(bottom=True, top=False, direction='inout')
        ax.yaxis.set_tick_params(left=True, right=False, direction='inout')

        # Center the graph and make it square
        ax.set_yticks([-1.0, -0.8, -0.6, -0.4, -0.2, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_xticks([-1.0, -0.8, -0.6, -0.4, -0.2, 0.2, 0.4, 0.6, 0.8, 1.0])

        # Draw a circle of radius 1
        circle1 = plt.Circle((0, 0), radius=1, color='black', fill=False)
        ax.add_artist(circle1)

        # Get colors for each vector arrow
        cmap = plt.cm.get_cmap('viridis', len(self.features))

        for feature in range(0, len(self.features)):
            # Get coordinates of the "arrow head" along both components
            x = self.pca.components_[components[0]-1, feature]
            y = self.pca.components_[components[1]-1, feature]

            # Compute coordinates for annotation
            anot_x = x + 0.05 if x > 0 else x - 0.05
            anot_y = y + 0.05 if y > 0 else y - 0.05

            ax.arrow(0, 0, # Vector arrow starts at (0, 0)
                     x, y, # Arrow head coordinates
                     color=cmap(feature),
                     head_width=0.03, head_length=0.03)

            # Add arrow annotation
            ax.annotate(self.features[feature],
                        xy=(anot_x, anot_y),
                        color=cmap(feature))

        # Get explained variances as percentage for each component
        exp_var_cp1 = round(self.pca.explained_variance_ratio_[components[0]-1]*100)
        exp_var_cp2 = round(self.pca.explained_variance_ratio_[components[1]-1]*100)

        # Label axes with the number of the PC and their % of explained variance
        ax.set_xlabel('PC {} ({}%)'.format(components[0], exp_var_cp1))
        ax.set_ylabel('PC {} ({}%)'.format(components[1], exp_var_cp2))

        # Move the axis labels to the edges of the graph
        ax.xaxis.set_label_coords(0.5, -0.03)
        ax.yaxis.set_label_coords(-0.03, 0.5)

        # Give us some room to breathe
        ax.set_xlim((-1.02, 1.02))
        ax.set_ylim((-1.02, 1.02))

        # Give the plot a title
        ax.set_title('Circle of correlations (PC{}xPC{})'.format(components[0],
                                                                 components[1]))

        if show:
            plt.show(ax)

        plt.close(fig)

    def match_data_transform(self):
        """Create a table to allow matching original data points with the
        transformed data and their coordinates on each component."""

        before = self.data[self.features]

        # Create dataframe of data after transformation
        after = pd.DataFrame(data=self.data_t,
                             index=range(0, len(self.data_t)),
                             columns=self.features)
        after = after.add_suffix('_t')

        # Create dataframe of coordinates along each component
        coord = pd.DataFrame(data=self.projected,
                             index=range(0, len(self.data_t)),
                             columns=['PC{}'.format(i+1) for i in range(len(self.pca.components_))])

        # Bind columns from after and before
        self.table = pd.concat([after.reset_index(drop=True), before], axis=1)

        # Sort columns alphabetically
        self.table = self.table[sorted(self.table.columns.tolist())]

        # Bind columns from projected data and table
        self.table = pd.concat([coord.reset_index(drop=True), self.table], axis=1)

        # Count number of occurences of each row and display it in 'n' column
        self.table = self.table.groupby(self.table.columns.tolist()).size().reset_index(name='n')

    def show_points(self, coords={1:0, 2:0}, around=0.25, show_all=False):
        """ Show data points with coordinates along PC axes.

        :coords: dict of coordinates
        :around: plus or minus
        :show_all: show all columns (normalized data and unused PCs)
        """

        table = self.table

        # Select data points with the coordinates
        for pc, coord in coords.items():
            col = 'PC{}'.format(pc)
            table = table[(table[col] >= coord-around) & (table[col] <= coord+around)]

        if not show_all:
            # Only keep relevant component coordinates
            pc_col = [c for c in table.columns if 'PC' in c]
            pc_col = [c for c in pc_col if int(c[-1]) not in coords.keys()]
            keep_cols = [c for c in table.columns if c not in pc_col]
            table = table[keep_cols]

            # Remove transformed data from table
            table = table[[c for c in table.columns if '_t' not in c]]

        print(table)