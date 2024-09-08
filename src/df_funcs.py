import pandas as pd


def identity_assurance_func(df, factors, emissions):
    """Ensures that the product of factors equals the emissions in the input dataframe.

    This function calculates the difference between the product of factors and
    the emissions, and checks if this difference (residual) is zero.

    Args:
        df (pandas.DataFrame): Dataframe with factors ready for composition.

    Returns:
        pandas.DataFrame: The input dataframe if the residual is zero.

    Raises:
        ValueError: If the factors are not equal to emissions (non-zero residual).
    """

    df["res"] = df[emissions] - df[factors].prod(axis=1).round(
        2
    )  # round to eliminate rounding errors

    # Assert that residuals are 0
    if df["res"].sum() == 0:
        return df
    else:
        raise ValueError("Factors are not equal to emissions")


def nested_dict_to_df(n_dict):
    """Converts a nested dictionary of results to a formatted DataFrame.

    Args:
        n_dict (dict): Nested dictionary with results.

    Returns:
        pandas.DataFrame: Dataframe with drivers as columns and sectors as index.

    Notes:
        The resulting DataFrame columns are reordered to:
        ['totGDP', 'sec_gdp/totGDP', 'totGWh/sec_gdp', 'fossGWh/totGWh', 'mtCO2e/fossGWh']
    """
    # Make dataframe from nested dict
    df = pd.concat({k: pd.DataFrame(v).T for k, v in n_dict.items()}, axis=1)

    # Drop multilevel columns
    df.columns = df.columns.droplevel()

    # reset index, tranpose dataframe
    df = df.reset_index().transpose()

    # set factors as column headers
    df.columns = df.iloc[0]

    # remove row containing column names, make dataframe into float
    df = df.iloc[1:, :].astype("float")

    return df


def df_to_nested_dict(df, key_col: str):
    """Converts a DataFrame to a nested dictionary based on unique sectors.

    Args:
        df (pandas.DataFrame): Input DataFrame containing a 'næring' column
                               representing sectors.

    Returns:
        dict: A nested dictionary where each key is a unique sector, and
              the corresponding value is a DataFrame containing data for that sector.

    Notes:
        The 'næring' column is used to identify unique sectors.
    """
    # create unique list of sectors
    sectors = df[key_col].unique()

    # create a data frame dictionary to store your data frames
    dfd = {elem: pd.DataFrame for elem in sectors}

    # Create nested dict where each dataframe containing sector number is key
    for key in dfd.keys():
        dfd[key] = df.loc[df[key_col] == key, :]

    return dfd  # dict containing dataframes


def rename_shift_func(df):
    """Shifts the year column in the results DataFrame by -1.

    This function adjusts the year column so that the results correspond
    to the correct time period in the LMDI analysis.

    Args:
        df (pandas.DataFrame): Input DataFrame with a year index.

    Returns:
        pandas.DataFrame: DataFrame with the year column shifted by -1 and
                          set as the index.

    Notes:
        The shift is done because the LMDI analysis result for year t
        represents the difference between t and t+1. For example, the
        result labeled as 1991 represents the change from 1990 to 1991.
    """
    df = df.reset_index()
    df = df.rename(columns={"index": "year"})
    year = df["year"].shift(-1).fillna(2019).astype("int")
    df["year"] = year
    df = df.set_index("year")

    return df

def result_sum_func(n_dict: dict[pd.DataFrame]):
    """Sums the results for each sector across all years to get the total change.

    This function processes a nested dictionary of results, summing the contributions
    of each driver within the results for each sector. It then restructures the data
    into a more accessible format.

    Args:
        n_dict (dict): A nested dictionary where keys are sectors and values are
                       DataFrames containing yearly results for different drivers.

    Returns:
        dict: A dictionary where keys are sectors and values are DataFrames.
              Each DataFrame contains the summed contributions of each driver
              for that sector, pivoted so that drivers are columns and there's
              a single row for the sector.

    Example:
        Input n_dict structure:
        {
            'sector1': DataFrame(yearly data for drivers),
            'sector2': DataFrame(yearly data for drivers),
            ...
        }

        Output d_sum structure:
        {
            'sector1': DataFrame(summed data, drivers as columns),
            'sector2': DataFrame(summed data, drivers as columns),
            ...
        }

    Note:
        The function assumes that the input dictionary's DataFrames have a consistent
        structure across all sectors.
    """
    # Function implementation remains the same
    sectors = list(n_dict.keys())
    d_sum = {}
    i = 0
    for k in n_dict:
        d_sum[k] = pd.DataFrame(n_dict[k].sum())
        d_sum[k]['sector'] = sectors[i]
        d_sum[k]['factor'] = d_sum[k].index
        d_sum[k] = d_sum[k].pivot(columns='factor', values=0, index='sector')
        i += 1
    return d_sum