import pandas as pd
from pca import ThreadPCA, log_norm_transform

threads = pd.read_csv('data/working/threads2017.csv')

def test_transform():
    log_norm_transform(threads[['star_nodes', 'deg_max', 'h_index', 'deg_max_2']])
