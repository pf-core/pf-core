"""

Pathfinder plotting module, @esteinig

Common plotting functions for workflow debugging. Main plots are handled with MongoAPI in Vue.

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas

from sklearn.linear_model import LinearRegression


def plot_date_randomisation(
    ax: plt.axes,
    replicates: np.array or list,
    rate: float,
    log10: bool = True
) -> plt.axes:

    """ Plot distribution of substitution rates for date randomisation test

    :param ax: axes object to plot the date randomisation
    :param replicates: list of replicate substitution rate estimates
    :param rate: true rate estimate vertical line for evaluation
    :param log10: plot log10 of substitution rates on horizontal axis

    :returns axes object

    """

    if log10:
        replicates = np.log10(replicates)

    with plt.style.context('seaborn-colorblind'):
        ax.hist(x=replicates, color='gray')
        ax.axvline(x=rate, color='r')

    return ax


def plot_regression(
    ax: plt.axes,
    regression_data: pandas.DataFrame,
) -> plt.axes:

    """ Plot regression between dates and root-to-tip distances

    Data corresponds to `rtt.csv` output from TimeTree clock regression.

    :param ax: axes object to plot on
    :param regression_data: data frame with dates (x-axis, column 0)
        and root-to-tip distances (x-axis, column 0)

    :returns axes object

    """

    x = regression_data.iloc[:, 0].values.reshape(-1, 1)  # 2-d
    y = regression_data.iloc[:, 1].values.reshape(-1, 1)
    linear_regressor = LinearRegression()
    linear_regressor.fit(x, y)
    y_pred = linear_regressor.predict(y)

    ax.scatter(x, y)
    ax.plot(x, y_pred, color='r')

    return ax
