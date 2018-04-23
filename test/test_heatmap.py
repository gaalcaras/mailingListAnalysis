import pandas as pd
import heatmap as ht
import matplotlib.pyplot as plt

threads = pd.read_csv('data/threads2017.csv')
small_t = threads[threads.emails == 10]

def test_heatmap_count():
    ht.heatmap_count(small_t, ['emails', 'users'], show=False)
    plt.clf()

def test_ordered_mosaic():
    ht.ordered_mosaic(small_t, ['h_index', 'users'], show=False)
    plt.clf()
