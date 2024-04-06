""" zid_project2_portfolio.py

"""

# ------------------------------------------------------------------------------------------------------------------
# Part 6: read and utilize portfolio construction functions in
#         zid_project2_portfolio.py to answer the questions in Part 7
# ------------------------------------------------------------------------------------------------------------------

import zid_project2_etl as etl
import zid_project2_characteristics as cha
import pandas as pd
import numpy as np
import util
import sys


def pf_input_sanity_check(df_cha, cha_name):

    """
    Performs sanity checks on the DataFrame and characteristic name inputs for portfolio construction.

    This function verifies:
    1. The `cha_name` is a valid string.
    2. The frequency of the DataFrame index is monthly (`period[M]`).
    3. The columns related to the characteristic name (`cha_name`) are correctly formatted and match
    the return columns in terms of naming and count.


    Parameters
    ----------
    df_cha : df
        A merged DataFrame with a Monthly frequency PeriodIndex, containing rows
        for each year-month that include the stock returns for that period and the characteristics
        from the previous year-month.
        See the docstring of the `merge_tables` function in zid_project2_characteristics.py
        for a description of this df.

    cha_name : str
        It is the name of the characteristic has been calculated.
        It is 'vol' when calculating total volatility.

    Returns
    ----------
    - None: Prints a success message if all checks pass. If any check fails, the program will terminate
    with an error message.

    Raises
    ----------
    - SystemExit: If `cha_name` is not a string, if the DataFrame does not meet the frequency requirement, and
    if column names are improperly formatted, the function halts execution with an appropriate error message.

    """

    # Check input table frequency and column names
    # import pdb; pdb.set_trace();
    # extract the position of first '_' in column names with suffix '_cha_name'
    position = -len('_{}'.format(cha_name))
    # prep for verify the columns related to the characteristic name (`cha_name`) are correctly formatted
    # and match the monthly return columns in terms of naming and count
    cols = list(df_cha.columns)
    tics = [i for i in df_cha.columns if i.find('_{}'.format(cha_name)) == -1]
    tics.sort()
    tics_cha = list(set(cols) - set(tics))
    tics_cha = [i[:position] for i in tics_cha]
    tics_cha.sort()

    # Check if cha_name is a string and corresponds to an existing function
    if not isinstance(cha_name, str):
        return sys.exit("`cha_name` must be a string")

    if df_cha.index.dtype == 'period[M]':
        print("df_cha table is in monthly frequency")
    else:
        sys.exit("Please make sure df_cha table is in monthly frequency")

    if tics_cha == tics:
        print("df_cha includes stocks' monthly returns and respective characteristics")
    else:
        sys.exit("Please make sure df_cha includes stocks' monthly returns and respective characteristics")

    return util.color_print('Sanity checks for inputs of long short portfolio construction passed')


def df_reshape(df_cha, cha_name):
    """
    Reshapes a DataFrame to consolidate return and characteristic columns for each ticker.

    This function reshapes `df_cha`, the output table of `cha_main` function in zid_project2_characteristics.py.
    `df_cha` has a Monthly frequency PeriodIndex. Each year-month row includes the monthly returns
    and the characteristics for all stocks. The resulting DataFrame also has a Monthly frequency
    PeriodIndex. It shows a consolidated view where each row represents a ticker,
    along with its returns and characteristic values in a year-month.

    Parameters
    ----------
    df_cha : df
        A Pandas data frame with monthly returns and the characteristics information.
        This df is the output of `cha_main` function in characteristics.py.
        See the docstring there for a description of it.

    cha_name : str
        The name of the characteristic.

    Returns
    -------
    df
        A reshaped DataFrame where each row corresponds to a specific ticker, including columns
        for monthly returns ('Ret'), the specified characteristic (named as f`{cha_name}`), and
        the ticker name.
        - df.columns: it has three columns: 'Ret', which contains monthly returns;
          `{cha_name}`, which holds the characteristics;
          and 'ticker', which identifies the stock ticker associated with the returns and characteristics.

        - df.index: Monthly frequency PeriodIndex with name of 'Year_Month'.

    Examples:
    Note: The examples below are for illustration purposes. Your ticker/sample
    period may be different.

    >> ret_dic = etl.aj_ret_dict(tickers = ['AAPL', 'TSLA', 'aal', 'abbv', 'bac'],\
                                      start = '2010-05-15', end = '2010-08-31')
    >> charc = cha.cha_main(ret_dict, 'vol', ['Daily',])
    >> _test_df_reshape(charc, 'vol')

       ----------------------------------------
       This means `df_reshaped = df_reshape(df, cha_name)`, print out df_reshaped:
                       Ret        vol ticker
       Year_Month
       2010-06    -0.020827       NaN   aapl
       2010-07     0.022741  0.019396   aapl
       2010-08    -0.055005  0.015031   aapl
       2010-06          NaN       NaN   tsla
       2010-07    -0.163240       NaN   tsla
       2010-08    -0.023069  0.065355   tsla
       2010-06    -0.024915       NaN    aal
       2010-07     0.260162  0.047429    aal
       2010-08    -0.166820  0.045688    aal
       2010-06          NaN       NaN   abbv
       2010-07          NaN       NaN   abbv
       2010-08          NaN       NaN   abbv
       2010-06    -0.086448       NaN    bac
       2010-07    -0.022964  0.022104    bac
       2010-08    -0.112536  0.028780    bac

       Obj type is: <class 'pandas.core.frame.DataFrame'>

       <class 'pandas.core.frame.DataFrame'>
       PeriodIndex: 15 entries, 2010-06 to 2010-08
       Freq: M
       Data columns (total 3 columns):
        #   Column  Non-Null Count  Dtype
       ---  ------  --------------  -----
        0   Ret     11 non-null     float64
        1   vol     7 non-null      float64
        2   ticker  15 non-null     object
       dtypes: float64(2), object(1)
        """
    # collect tics
    tickers = [i for i in df_cha.columns if i.find('_{}'.format(cha_name)) == -1]
    df_collect = pd.DataFrame()
    # iterate tics and reshape table
    for ticker in tickers:
        temp = df_cha[[ticker, ticker + '_{}'.format(cha_name)]]
        temp = temp.rename({'{}'.format(ticker): 'Ret',
                            '{}_{}'.format(ticker, cha_name): '{}'.format(cha_name)}, axis=1)
        temp['ticker'] = '{}'.format(ticker)
        df_collect = pd.concat([df_collect, temp], axis=0)

    df_reshaped = df_collect.copy()

    util.color_print('df_reshape function done')
    return df_reshaped


def stock_sorting(df_reshaped, cha_name, q):
    """
    Sorts stocks into quantiles within each year-month based on a specified characteristic.

    This function groups the input table, `df_reshaped`, by its PeriodIndex and applies a quantile cut
    to the specified characteristic, dividing the stocks into `q` quantiles.
    Each stock is assigned a rank based on which quantile its characteristic value falls into. The ranks
    are then merged back into the input DataFrame, creating a sorted DataFrame with an additional 'rank' column.

    Parameters
    ----------
    - df_reshaped : df
        A DataFrame containing monthly returns, characteristic and stock ticker.
        This df is the output of `df_reshape` function in this script. See the docstring there
        for a description of it.

    - cha_name : str
        The name of the characteristic.

    - q : int
        The number of quantiles to divide the stocks into based on their characteristic values.

    Returns
    -------
    df
        The output table is an updated `df_reshaped` table with an added 'rank' column
        indicating the quantile rank of each stock within a year-month,
        based on the specified characteristic.


    Examples:
    Note: The examples below are for illustration purposes. Your ticker/sample
    period may be different.

    >>  ret_dict = etl.aj_ret_dict(tickers=['AAPL', 'TSLA', 'aal', 'abbv', 'bac'],
                               start='2010-05-15', end='2010-08-31')
    >>  charc = cha.cha_main(ret_dict, 'vol', ['Daily',])
    >>  _test_stock_sorting(charc, 'vol', 2)
       ----------------------------------------
       This means `df_sorted = stock_sorting(df, cha_name, q), print out df_sorted:

                       Ret       vol  ticker  rank
       Year_Month
       2010-07    0.022741  0.019396   aapl     0
       2010-07   -0.022964  0.022104    bac     0
       2010-07    0.260162  0.047429    aal     1
       2010-08   -0.055005  0.015031   aapl     0
       2010-08   -0.112536  0.028780    bac     0
       2010-08   -0.166820  0.045688    aal     1
       2010-08   -0.023069  0.065355   tsla     1

       Obj type is: <class 'pandas.core.frame.DataFrame'>

       <class 'pandas.core.frame.DataFrame'>
       PeriodIndex: 7 entries, 2010-07 to 2010-08
       Freq: M
       Data columns (total 4 columns):
        #   Column  Non-Null Count  Dtype
       ---  ------  --------------  -----
       0   Ret     7 non-null      float64
       1   vol     7 non-null      float64
       2   ticker  7 non-null      object
       3   rank    7 non-null      int64
       dtypes: float64(2), int64(1), object(1)

    """

    df_reshaped.dropna(inplace=True)
    rank_ser = df_reshaped.groupby(level=0)['{}'.format(cha_name)]\
        .transform(lambda x: pd.qcut(x, q, labels=False, duplicates='drop')).rename('rank')
    df_sorted = pd.concat([df_reshaped, rank_ser], axis=1)
    df_sorted.dropna(inplace=True)

    util.color_print('stock_sorting function done')
    return df_sorted


def pf_cal(df_sorted, cha_name, q):
    """
    Calculates the equal-weighted portfolios for each quantile in the input table, `df_sorted`,
    and then construct the long-short portfolio.

    This function groups the `df_sorted` by table index and the `rank` column,
    calculates the equally weighted(ew)/average returns of each quantile in every year-month,
    and constructs a long-short portfolio by subtracting the year-month ew return of
    the first quantile from that of the last quantile.

    Parameters
    ----------
    df_sorted : df
        A Pandas data frame with monthly returns, the characteristics and ranking information.
        This df is the output of `stock_sorting` function in this script. See the docstring there
        for a description of it.
    cha_name : str
        The name of the characteristic.
    q : int
        The number of quantiles that the stocks in `df_sorted` been divided into
        based on their characteristic values.

    Returns
    -------
    df
        A DataFrame containing the ew portfolio of each quantile and the long-short portfolio,
        The DataFrame has monthly PeriodIndex.
        - df.columns: the ew portfolio return series of each quantile (with prefix 'ewp_rank_') and
          the long-short portfolio return series('ls').
          For example, there will be 3 columns in resulting df when `q` equal to 2:
          'ewp_rank_1', 'ewp_rank_2', and 'ls'
        - df.index: Monthly frequency PeriodIndex with name of 'Year_Month'.
          It contains all PeriodIndex year_month of the `df_sorted` data frame.

    Examples:
    Note: The examples below are for illustration purposes. Your ticker/sample
    period may be different.

    >> ret_dict = etl.aj_ret_dict(tickers=['AAPL', 'TSLA', 'aal', 'abbv', 'bac'],
                                  start='2010-05-15', end='2010-08-31')
    >> charc = cha.cha_main(ret_dict, 'vol', ['Daily',])
    >> _test_pf_cal(charc, 'vol', 2)
       ----------------------------------------
       This means `df_f = pf_cal(df_sorted, cha_name, q)`
       `df_f_transpose = df_f.T`
       The value of `df_f_transpose` is
       Year_Month       2010-07   2010-08
       ewp_rank_1     -0.000112 -0.083770
       ewp_rank_2      0.260162 -0.094945
       ls              0.260274 -0.011174

       ----------------------------------------
       df_f  info:

       <class 'pandas.core.frame.DataFrame'>
       PeriodIndex: 2 entries, 2010-07 to 2010-08
       Freq: M
       Data columns (total 3 columns):
        #   Column          Non-Null Count  Dtype
       ---  ------          --------------  -----
        0   ewp_rank_1      2 non-null      float64
        1   ewp_rank_2      2 non-null      float64
        2   ls              2 non-null      float64
       dtypes: float64(6)

    """
    portfolio_ret = df_sorted.groupby([df_sorted.index.name, 'rank'])['Ret']\
        .mean().to_frame('_ew').reset_index(level='rank')

    lst = []
    for i in range(q):
        temp = portfolio_ret[portfolio_ret['rank'] == float(i)]\
            .drop('rank', axis=1)\
            .rename({'_ew': 'ewp_rank_{}'.format(i+1)}, axis=1)

        lst += [temp]

    df = pd.concat(lst, axis=1)
    df['ls'] = df['ewp_rank_{}'.format(q)] - df['ewp_rank_1']

    util.color_print('pf_cal function done')
    return df


def pf_main(df_cha, cha_name, q):
    """
    Constructs portfolios based on the specified characteristic and quantile threshold.

    This function performs several steps to construct a portfolio:
    1. Call `pf_input_sanity_check` function to check the sanity of inputs to ensure
       they meet required formats and constraints.
    2. Call `df_reshape` function to reshapes the input DataFrame `df_cha`
       to align with the processing needs for the third step, stock sorting.
    3. Call `stock_sorting` function to sort stocks and give them a ranking.
    4. Cal `pf_cal` function to constructs equal weighted long-short portfolios
       using sorted stock table from step 3

    Parameters
    ----------
    df_cha : df
        A Pandas data frame with stock monthly returns and the characteristics information.
        This df is the output of `cha_main` function in zid_project2_characteristics.py.
        See the docstring there for a description of it.
    cha_name : str
        The name of the characteristic. Here, it should be 'vol'
    q : int
        The number of quantiles to divide the stocks into based on their characteristic values.

    Returns
    -------
    df
        A DataFrame containing the constructed equal-weighted quantile and long-short portfolios.

    Note:
    The function internally calls `pf_input_sanity_check`, `df_reshape`, `stock_sorting`, and `pf_cal` functions.
    Ensure these functions are defined and correctly implemented.
    """

    # sanity check for inputs
    pf_input_sanity_check(df_cha, cha_name)

    # reshape the characteristic df
    df_reshaped = df_reshape(df_cha, cha_name)

    # stock sorting
    df_sorted = stock_sorting(df_reshaped, cha_name, q)

    # portfolio construction
    df_f = pf_cal(df_sorted, cha_name, q)

    util.color_print('portfolio script done')
    return df_f


def _test_df_cha_gen():
    """ Function for generating made-up dataframe output from characteristics.py.
        Update the made-up dataframe as necessary when testing functions.
    """
    idx = pd.to_datetime([
        '2019-01-31', '2019-02-28', '2019-03-31', '2019-04-30', '2019-05-31',
    ]).to_period('M')

    stock1 = [ 0.023969,  0.005083, -0.021728,  np.nan,     np.nan,  ]
    stock2 = [ 0.013220,  0.014490, -0.045329,  0.024182,  0.009146, ]
    stock3 = [ np.nan,    0.029547,  0.011807,  np.nan,     0.010892, ]
    stock4 = [-0.021478, -0.041856,  0.031371,  np.nan,    -0.023821, ]

    stock1_cha_name = [ np.nan,  0.001823,  0.000826, -0.004043,  np.nan,   ]
    stock2_cha_name = [ np.nan, -0.006415,  0.038704, -0.035984,  0.008183, ]
    stock3_cha_name = [ np.nan,  np.nan,   -0.036619, -0.025764,  np.nan,   ]
    stock4_cha_name = [ np.nan,  0.037371, -0.011854, -0.023779,  np.nan,   ]

    madeup_df_cha = pd.DataFrame(data={'stock1': stock1, 'stock2': stock2, 'stock3': stock3, 'stock4': stock4,
                                        'stock1_cha_name': stock1_cha_name, 'stock2_cha_name': stock2_cha_name,
                                        'stock3_cha_name': stock3_cha_name, 'stock4_cha_name': stock4_cha_name,
                                       },
                                index=idx)
    madeup_df_cha.index.name = 'Year_Month'
    return madeup_df_cha


def _test_pf_input_sanity_check(df_cha, cha_name):
    """ Test function for `pf_input_sanity_check`
    """
    pf_input_sanity_check(df_cha, cha_name)


def _test_df_reshape(df_cha,cha_name):
    """ Test function for `df_reshape`
    Examples:
    >> made_up_df_cha = _test_df_cha_gen()
    >> _test_df_reshape(made_up_df_cha, 'cha_name')

       ----------------------------------------
       This means `df_reshaped = df_reshape(df_cha, cha_name)`, print out df_reshaped:

                        Ret  cha_name  ticker
       Year_Month
       2019-01     0.023969       NaN  stock1
       2019-02     0.005083  0.001823  stock1
       2019-03    -0.021728  0.000826  stock1
       2019-04          NaN -0.004043  stock1
       2019-05          NaN       NaN  stock1
       ...
       2019-01    -0.021478       NaN  stock4
       2019-02    -0.041856  0.037371  stock4
       2019-03     0.031371 -0.011854  stock4
       2019-04          NaN -0.023779  stock4
       2019-05    -0.023821       NaN  stock4

       Obj type is: <class 'pandas.core.frame.DataFrame'>

       <class 'pandas.core.frame.DataFrame'>
       PeriodIndex: 20 entries, 2019-01 to 2019-05
       Freq: M
       Data columns (total 3 columns):
        #   Column    Non-Null Count  Dtype
       ---  ------    --------------  -----
        0   Ret       15 non-null     float64
        1   cha_name  12 non-null     float64
        2   ticker    20 non-null     object
       dtypes: float64(2), object(1)
       memory usage: 640.0+ bytes
       ----------------------------------------
    """
    df_reshaped = df_reshape(df_cha, cha_name)

    msg = "This means `df_reshaped = df_reshape(df_cha, cha_name)`, print out df_reshaped:"
    util.test_print(df_reshaped, msg)


def _test_stock_sorting(df_cha, cha_name, q):
    """ Test function for `stock_sorting`
    Examples:
    >> made_up_df_cha = _test_df_cha_gen()
    >> _test_stock_sorting(made_up_df_cha, 'cha_name', 2)
       ----------------------------------------
       This means `df_sorted = stock_sorting(df, cha_name, q)`, print out df_sorted:

                        Ret  cha_name  ticker  rank
       Year_Month
       2019-02     0.014490 -0.006415  stock2   0.0
       2019-02     0.005083  0.001823  stock1   0.0
       2019-02    -0.041856  0.037371  stock4   1.0
       2019-03     0.011807 -0.036619  stock3   0.0
       2019-03     0.031371 -0.011854  stock4   0.0
       2019-03    -0.021728  0.000826  stock1   1.0
       2019-03    -0.045329  0.038704  stock2   1.0

       Obj type is: <class 'pandas.core.frame.DataFrame'>

       <class 'pandas.core.frame.DataFrame'>
       PeriodIndex: 7 entries, 2019-02 to 2019-03
       Freq: M
       Data columns (total 4 columns):
        #   Column    Non-Null Count  Dtype
       ---  ------    --------------  -----
        0   Ret       7 non-null      float64
        1   cha_name  7 non-null      float64
        2   ticker    7 non-null      object
        3   rank      7 non-null      float64
       dtypes: float64(3), object(1)
       memory usage: 280.0+ bytes
       ----------------------------------------

    """
    df_reshaped = df_reshape(df_cha, cha_name)
    df_sorted = stock_sorting(df_reshaped, cha_name, q)

    msg = "This means `df_sorted = stock_sorting(df, cha_name, q)`, print out df_sorted:"
    print_table = df_sorted.sort_values([df_reshaped.index.name, '{}'.format(cha_name)])
    util.test_print(print_table, msg)


def _test_pf_cal(df_cha, cha_name, q):
    """ Test function for `pf_cal`
    Examples:
    >> made_up_df_cha = _test_df_cha_gen()
    >> _test_pf_cal(made_up_df_cha, 'cha_name', 2,)
       ----------------------------------------
       This means `df_f = pf_cal(df_sorted, cha_name, q)`
       `df_f_transpose = df_f.T`
       The value of `df_f_transpose` is
       Year_Month   2019-02   2019-03
       ewp_rank_1  0.009787  0.021589
       ewp_rank_2 -0.041856 -0.033529
       ls         -0.051642 -0.055117
       ----------------------------------------
       df_f  info:

       <class 'pandas.core.frame.DataFrame'>
       PeriodIndex: 2 entries, 2019-02 to 2019-03
       Freq: M
       Data columns (total 3 columns):
        #   Column      Non-Null Count  Dtype
       ---  ------      --------------  -----
        0   ewp_rank_1  2 non-null      float64
        1   ewp_rank_2  2 non-null      float64
        2   ls          2 non-null      float64
       dtypes: float64(3)
       memory usage: 64.0 bytes
    """
    df_reshaped = df_reshape(df_cha, cha_name)
    df_sorted = stock_sorting(df_reshaped, cha_name, q)
    df_f = pf_cal(df_sorted, cha_name, q)
    df_f_transpose = df_f.T
    to_print = [
        "This means `df_f = pf_cal(df_sorted, cha_name, q)`",
        "`df_f_transpose = df_f.T`\n"
        f"The value of `df_f_transpose` is \n{df_f_transpose}",
    ]
    util.test_print('\n'.join(to_print))
    print("df_f  info:\n")
    df_f.info()

    return df_f


def _test_pf_main(df_cha, cha_name, q):
    """ Test function for `pf_main`
    """
    df_ls = pf_main(df_cha, cha_name, q)
    print(df_ls)


if __name__ == "__main__":
    pass

    # # use made-up characteristic dataframe, _test_ret_dic_gen, to test functions:
    # made_up_df_cha = _test_df_cha_gen()
    # _test_pf_input_sanity_check(made_up_df_cha, 'cha_name')
    #
    # _test_df_reshape(made_up_df_cha, 'cha_name')
    # _test_stock_sorting(made_up_df_cha, 'cha_name', 2)
    # _test_pf_cal(made_up_df_cha, 'cha_name', 2,)
    # _test_pf_main(made_up_df_cha, 'cha_name', 2)

    # # use test return dict and cha df to test functions:
    # ret_dict = etl.aj_ret_dict(tickers=['AAPL', 'TSLA', 'aal', 'abbv', 'bac'],
    #                            start='2010-05-15', end='2010-08-31')
    # charc = cha.cha_main(ret_dict, 'vol', ['Daily',])
    # # #
    # _test_pf_input_sanity_check(charc, 'vol')
    # _test_df_reshape(charc, 'vol')
    # _test_stock_sorting(charc, 'vol', 2)
    # _test_pf_cal(charc, 'vol', 2)
    # _test_pf_main(charc, 'vol', 2)
