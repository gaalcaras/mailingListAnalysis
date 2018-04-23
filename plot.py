import matplotlib.pyplot as plt

def scatter(df, var_list, log=True, show=True):
    x = df[var_list[0]]
    y = df[var_list[1]]

    sc = plt.scatter(x, y)
    x_label = var_list[0]
    y_label = var_list[1]

    if log:
        sc.axes.set_xscale('log')
        sc.axes.set_yscale('log')
        x_label += ' (log scale)'
        y_label += ' (log scale)'

    sc.axes.set_xlabel(x_label)
    sc.axes.set_ylabel(y_label)

    if show:
        plt.show()
