import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def barplot_additive_aggregate(df, factors):
    """
    Create a bar plot showing the additive aggregate effect of drivers on total emissions.

    This function sets up a seaborn plot style, creates a bar plot using the input data,
    sets the y-axis label, adds a title, and displays the plot.

    Args:
        df (pandas.DataFrame): The dataframe containing the data to be plotted.
        factors (list): A list of factors (not currently used in the function).

    Returns:
        None: This function displays the plot but does not return any value.
    """
    sns.set_theme(style='whitegrid', rc={'figure.figsize':(12,6)})
    plot = sns.barplot(data=df, palette='crest', errorbar=None)
    plot.set(ylabel='Million tonnes CO2e')
    plt.suptitle('Absolute effect of drivers on total emissions, 1990 - 2019', size=18)
    plt.show()

def heatmapper_func(df, factors, sectors):
    """
    Create a heatmap showing the contribution of drivers to emissions.

    This function calculates total emissions change, creates a mask for the heatmap,
    sets up the plot style, creates two overlapping heatmaps (one for color and one for annotations),
    adds labels and a title, and displays the plot.

    Args:
        df (pandas.DataFrame): The dataframe containing the data to be plotted.
        factors (list): A list of factors to be used as x-axis labels.
        sectors (list): A list of sectors to be used as y-axis labels.

    Returns:
        pandas.DataFrame: The input dataframe with an additional 'total emissions change' column.
    """
    df['total emissions change'] = df.sum(axis=1)
    
    mask = np.zeros((10, 6))
    mask[:,5] = True
    
    sns.set_theme(rc={'figure.figsize':(16, 8)}, style="whitegrid")
    
    sns.heatmap(df, mask=mask, cbar=True, cmap="Spectral_r")
    plt.suptitle('Contribution of drivers, 1990-2019', y=0.95, x=0.4, size=24)
    sns.heatmap(df, alpha=0, cbar=False, annot=True,
                annot_kws={"size": 16, "color":"orange"}, fmt='g',
                xticklabels=factors, yticklabels=sectors)
    plt.xlabel('Factor')
    plt.show()
    
    return df

def barplot_additive_drivers(df, sectors, title):
    """
    Create a horizontal bar plot showing additive drivers.

    This function sets up a seaborn plot style, creates a horizontal bar plot using the input data,
    sets axis labels, adds a title, and displays the plot.

    Args:
        df (pandas.DataFrame or array-like): The data to be plotted.
        sectors (str): The label for the y-axis.
        title (str): The title for the plot.

    Returns:
        None: This function displays the plot but does not return any value.
    """
    df = pd.DataFrame(df)
    sns.set_theme(style='whitegrid', rc={'figure.figsize':(10,5)})
    plot = sns.barplot(y=df.index, x=df.iloc[:,0], palette='mako', hue=df.index, legend=False)
    plot.set(ylabel=sectors, xlabel='Million tonnes CO2e')
    plt.suptitle(title, size=18)
    plt.show()