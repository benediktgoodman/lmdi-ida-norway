import numpy as np
import pandas as pd
from typing import Dict, List


# Skeleton class from xiwang2718 for doing LMDI-IDA
class PyLMDI:
    """Performs Log-Mean Divisia Index (LMDI) Index Decomposition Analysis (IDA).

    This class implements the LMDI method for decomposing changes in aggregate
    measures (e.g., emissions) into contributions from various factors.

    Attributes:
        V0 (list): Initial values of the aggregate measure.
        Vt (list): Final values of the aggregate measure.
        X0 (list of lists): Initial values of the factors.
        Xt (list of lists): Final values of the factors.

    Methods:
        Lfun: Calculates the logarithmic mean of two numbers.
        Xfun: Calculates the logarithmic ratio of two numbers.
        Add: Performs additive decomposition.
        Mul: Performs multiplicative decomposition.

    Note:
        The implementation is based on the work by xiwang2718.
    """

    def __init__(self, Vt, V0, Xt, X0):
        """Initializes the PyLMDI instance with input data.

        Args:
            Vt (list): Final values of the aggregate measure.
            V0 (list): Initial values of the aggregate measure.
            Xt (list of lists): Final values of the factors.
            X0 (list of lists): Initial values of the factors.
        """
        self.V0 = V0
        self.Vt = Vt
        self.X0 = X0
        self.Xt = Xt

    @staticmethod
    def Lfun(yt, y0):
        """Calculates the logarithmic mean of two numbers.

        Args:
            yt (float): Final value.
            y0 (float): Initial value.

        Returns:
            float: Logarithmic mean of yt and y0.
        """

        if yt == y0:
            return 0
        else:
            return (yt - y0) / (np.log(yt) - np.log(y0))

    @staticmethod
    def Xfun(xt, x0):
        """Calculates the logarithmic ratio of two numbers.

        Args:
            xt (float): Final value.
            x0 (float): Initial value.

        Returns:
            float: Logarithmic ratio of xt to x0.
        """
        if x0 == 0:
            return 1
        elif xt == 0:
            return 1
        else:
            return np.log(xt / x0)

    # Additive decomposition, yields LMDI-IDA across two time periods for one factor
    def Add(self):
        """Performs additive decomposition.

        Returns:
            list: LMDI-IDA results for changes in aggregate measure and factors.
        """
        Delta_V = [
            sum(self.Vt) - np.sum(self.V0)
        ]  # Changes in aggregate measure (emissions)
        for start, end in zip(self.X0, self.Xt):  # Vector of other factors
            temp = sum(
                [
                    self.Lfun(self.Vt[i], self.V0[i]) * np.log(end[i] / start[i])
                    for i in range(len(start))
                ]
            )
            Delta_V.append(temp)
        return Delta_V

    def Mul(self):
        """Performs multiplicative decomposition.

        Returns:
            list: LMDI-IDA results for relative changes in aggregate measure and factors.

        """
        D_V = [sum(self.Vt) / np.sum(self.V0)]
        for start, end in zip(self.X0, self.Xt):
            temp = sum(
                [
                    self.Lfun(self.Vt[i], self.V0[i])
                    / self.Lfun(sum(self.Vt), sum(self.V0))
                    * np.log(end[i] / start[i])
                    for i in range(len(start))
                ]
            )
            D_V.append(np.exp(temp))
        return D_V


class LMDI_single_step:
    """
    Performs Log-Mean Divisia Index (LMDI) decomposition for a single time step.

    This class calculates the LMDI decomposition between two consecutive years
    for a given dataset and set of drivers.

    Attributes:
        df (pd.DataFrame): Input DataFrame containing the data.
        year (int): Starting year for the decomposition.
        mode (str): Decomposition mode ('add' for additive, 'mul' for multiplicative).
        drivers (List[str]): List of driver column names.
        year_col (str): Name of the column containing year data.
        emissions_col (str): Name of the column containing emissions data.
    """

    def __init__(self, df: pd.DataFrame, year: int, mode: str, drivers: List[str], year_col: str, emissions_col: str):
        """
        Initialize the LMDI_single_step instance.

        Args:
            df (pd.DataFrame): Input DataFrame containing the data.
            year (int): Starting year for the decomposition.
            mode (str): Decomposition mode ('add' or 'mul').
            drivers (List[str]): List of driver column names.
            year_col (str): Name of the column containing year data.
            emissions_col (str): Name of the column containing emissions data.
        """
        self.df = df
        self.year = year
        self.mode = mode
        self.drivers = drivers
        self.year_col = year_col
        self.emissions_col = emissions_col

    def LMDI_decomposer(self) -> Dict[str, float]:
        """
        Perform LMDI decomposition for the current time step.

        Returns:
            Dict[str, float]: A dictionary containing the decomposition results
                              for each driver.
        """
        df0 = self.df[self.df[self.year_col] == self.year].set_index(self.year_col)
        df1 = self.df[self.df[self.year_col] == self.year + 1].set_index(self.year_col)

        C0 = df0[self.emissions_col].tolist()
        Ct = df1[self.emissions_col].tolist()
        X0 = df0[self.drivers].values.reshape([-1, 1])
        Xt = df1[self.drivers].values.reshape([-1, 1])

        LMDI = PyLMDI(Ct, C0, Xt, X0)
        ans = LMDI.Add() if self.mode == "add" else LMDI.Mul()

        results = {driver: value for driver, value in zip(self.drivers, ans[1:])}
        return results

class LMDI_analysis:
    """
    Performs LMDI analysis over a range of years.

    This class extends LMDI_single_step to perform decomposition analysis
    over multiple years, aggregating the results into a single DataFrame.

    Attributes:
        df (pd.DataFrame): Input DataFrame containing the data.
        start (int): Start year for the analysis.
        stop (int): End year for the analysis.
        mode (str): Decomposition mode ('add' for additive, 'mul' for multiplicative).
        drivers (List[str]): List of driver column names.
        year_col (str): Name of the column containing year data.
        emissions_col (str): Name of the column containing emissions data.
    """

    def __init__(self, df: pd.DataFrame, start: int, stop: int, mode: str, drivers: List[str], year_col: str, emissions_col: str):
        """
        Initialize the LMDI_analysis instance.

        Args:
            df (pd.DataFrame): Input DataFrame containing the data.
            start (int): Start year for the analysis.
            stop (int): End year for the analysis.
            mode (str): Decomposition mode ('add' or 'mul').
            drivers (List[str]): List of driver column names.
            year_col (str): Name of the column containing year data.
            emissions_col (str): Name of the column containing emissions data.
        """
        self.df = df.copy()
        self.start = start
        self.stop = stop
        self.mode = mode
        self.drivers = drivers
        self.year_col = year_col
        self.emissions_col = emissions_col
    
    def LMDI_analysis_func(self) -> pd.DataFrame:
        """
        Perform LMDI analysis over the specified range of years.

        Returns:
            pd.DataFrame: A DataFrame containing the decomposition results
                          for each year and driver.
        """
        res = []
        for year in range(self.start, self.stop):
            single_step = LMDI_single_step(self.df, year, self.mode, self.drivers, self.year_col, self.emissions_col)
            res.append(single_step.LMDI_decomposer())
        
        result = pd.DataFrame(res, index=range(self.start, self.stop))
        return result