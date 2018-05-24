import pandas as pd
from pca import ThreadPCA, log_norm_transform

threads = pd.read_csv('data/working/threads2017_labeled.csv')
threads = threads[threads.depth > 0]

def test_transform():
    log_norm_transform(threads[['star_nodes', 'deg_max', 'h_index', 'deg_max_2']])

def test_pca():
    pca = ThreadPCA(threads, ['star_nodes', 'deg_max', 'h_index', 'deg_max_2'])

def test_pca_scatter():
    pca = ThreadPCA(threads, ['star_nodes', 'deg_max', 'h_index', 'deg_max_2'])
    pca.scatter(show=False)
    pca.scatter(color='h_index', show=False)
    pca.scatter(color='category', show=False)

def test_scree():
    pca = ThreadPCA(threads, ['star_nodes', 'deg_max', 'h_index', 'deg_max_2'])
    pca.scree(show=False)

def test_corr_circle():
    pca = ThreadPCA(threads, ['star_nodes', 'deg_max', 'h_index', 'deg_max_2'])
    pca.corr_circle(show=False)
    pca.corr_circle(components=(1, 3), show=False)
