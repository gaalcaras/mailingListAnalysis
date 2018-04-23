import seaborn as sns
import numpy as nmp
import matplotlib.pyplot as plt
import pandas as pd
from tools import square_list, int_list

def heatmap_count(df, var_list, show=True):
    """Draw heatmap count of two variables"""

    # Count unique rows
    count = df.groupby(var_list).size().reset_index(name='n')
    count = count.pivot(*var_list, 'n')
    sns.heatmap(count)

    if show:
        plt.show()

def ordered_mosaic(df, var_list, show=True):
    """Ordered mosaic"""

    # Get values sorted by variables
    mosaic = df[var_list].sort_values(var_list).values

    # Labels for annotation
    labels = ['|'.join([str(elt) for elt in pair]) for pair in mosaic]

    # Prepare the matrix with dummy values
    values = int_list(labels)

    # Give the values and the labels the same shape
    values = nmp.array(square_list(values))
    labels = nmp.array(square_list(labels))

    mosaic = sns.heatmap(values, annot=labels, fmt='', cbar=False,
                         xticklabels=False, yticklabels=False)
    mosaic.set_title('Descending ordered list of {} | {}'.format(*var_list))

    if show:
        plt.show()
