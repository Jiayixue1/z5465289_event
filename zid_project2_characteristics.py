""" zid_project2_characteristics.py

"""

# ----------------------------------------------------------------------------
# Part 5.1: import needed modules
# ----------------------------------------------------------------------------
# Create import statements to import all modules you need in this script
# Note: please keep the aliases consistent throughout the project.
#       For details, review the import statements in zid_project2_main.py

# <COMPLETE THIS PART>


# ----------------------------------------------------------------------------------------
# Part 5.3: read the vol_input_sanity_check function
#           and use it to test if the inputs of zid_project2_characteristics are proper
# ----------------------------------------------------------------------------------------

def vol_input_sanity_check(ret, cha_name, ret_freq_use: list):
    """
    Performs sanity checks on the inputs provided for calculating stock characteristics.

    This function validates the inputs required for characteristic calculation, ensuring they meet specific criteria:
    - `dic_ret` must be a dictionary containing two keys: "Daily" and "Monthly".
    - `cha_name` must be a string and should correspond to a function name that exists
       for calculating the characteristic.
    - `ret_freq_use` should be a list containing any combination of "Daily" and "Monthly",
       or be empty to indicate which return series to be used when construct characteristics.

    Parameters
    ----------
    ret : dict
        A dictionary containing two items, where each item is a DataFrame that provides daily and monthly returns.
        See the docstring of the `aj_ret_dict` function in etl.py for a description of this dictionary.
    cha_name  :  str
        The name of the characteristic being calculated.
    ret_freq_use  :  list
        It identifies that which frequency returns you will use in following function to calculate the characteristic.


    Returns
    -------
    - None: If all checks pass, the function prints a success message and returns None.
      If any check fails, the program will terminate with an error message.

    Raises:
    - SystemExit: If any of the input validations fail, the function halts the program execution
      with an appropriate error message.
    """
    keys = {"Daily", "Monthly"}
    # Check if dic_ret is a dictionary with "Daily" and "Monthly" keys
    if not isinstance(ret, dict) or set(ret.keys()) != keys:
        return sys.exit("The input file, `ret`, must be a dictionary with two keys: 'Daily' and 'Monthly'.")

    # Check if cha_name is a string and corresponds to an existing function
    if not isinstance(cha_name, str):
        return sys.exit("`cha_name` must be a string")

    function_name = cha_name + "_cal"
    if function_name not in globals() or not callable(globals()[function_name]):
        return sys.exit("{} must be an existing function to calculate the characteristic.".format(function_name))

    # Check if ret_freq_use is a subset of {"Daily", "Monthly"}
    if not isinstance(ret_freq_use, list) or not set(ret_freq_use).issubset(keys):
        return sys.exit("`ret_freq_use` must be a list containing 'Daily', 'Monthly', both or blank.")

    return util.color_print('Sanity checks for inputs of characteristics script passed.')


# ----------------------------------------------------------------------------
# Part 5.4: Complete the vol_cal function
# ----------------------------------------------------------------------------
def vol_cal(ret, cha_name, ret_freq_use: list):
    """
    This function calculates the monthly total return volatility for stocks.
    It extracts daily return series, as specified by ret_freq_use, from the input dictionary named `ret`.
    Then, it calculates total return volatility (standard deviation) for each stock in each month.
    If a stock has fewer than 18 return entries in a month, the volatility value for that month
    is set to None.

    The return dictionary, `ret`, is generated from aj_ret_dict function in etl script, with its parameters,
    `tickers`, `start`, and `end`, determining the stock coverage and the sample period.

    Parameters
    ----------
    ret : dict
        A dictionary containing two items, where each item is a DataFrame that provides daily and monthly returns.
        See the docstring of the `aj_ret_dict` function in etl.py for a description of this dictionary.
    cha_name  :  str
        It is the name of the characteristic being calculated, which will be appended to the
        column names in the result DataFrame. Set it as 'vol' when calculating total volatility.
    ret_freq_use  :  list
        It identifies that which frequency returns you will use in this function.
        Set it as ['Daily',] when calculating total volatility.

    Returns
    -------
    df
        A DataFrame containing monthly total volatility values for each stock,
        where the volatility value will be set to None if the number of daily returns
        for the stock in that year-month is less than 18.

        - df.columns: All columns in the return dataframe are used from the input dictionary `ret`,
          but with the suffix f"_{cha_name}" added.

        - df.index: Monthly frequency PeriodIndex with name of 'Year_Month'

    Note: Please delete rows with **ALL** NaN value. Read pandas.DataFrame.dropna method documentation.

    Examples:
    Note: The examples below are for illustration purposes. Your ticker/sample
    period may be different.

    >> ret_dict = etl._test_aj_ret_dict(tickers=['AAPL', 'TSLA'], start='2010-05-15', end='2010-08-31')
    >> _test_vol_cal(ret_dict, 'vol', ['Daily',])

        ----------------------------------------
        This means `df_cha = vol_cal(ret, cha_name, ret_freq_use)`, print out df_cha:

                  aapl_vol  tsla_vol
        Year_Month
        2010-06   0.019396       NaN
        2010-07   0.015031  0.065355
        2010-08   0.012806  0.033770

        Obj type is: <class 'pandas.core.frame.DataFrame'>

        <class 'pandas.core.frame.DataFrame'>
        PeriodIndex: 3 entries, 2010-06 to 2010-08
        Freq: M
        Data columns (total 2 columns):
         #   Column    Non-Null Count  Dtype
        ---  ------    --------------  -----
         0   aapl_vol  3 non-null      float64
         1   tsla_vol  2 non-null      float64
        dtypes: float64(2)
        memory usage: 72.0 bytes
        ----------------------------------------

    Hints:
     -----
     - when you use dataframes in the return dictionary, use copy() method to create a new object
       ensuring that modifications to the copied DataFrame do not affect the original DataFrame stored in the dictionary
     - Read to_period() documentations before converting DatetimeIndex to PeriodIndex

    """

    # <COMPLETE THIS PART>


# ----------------------------------------------------------------------------
# Part 5.5: Complete the merge_tables function
# ----------------------------------------------------------------------------
def merge_tables(ret, df_cha, cha_name):
    """ This function merges `ret` and `df_cha` tables.
    It extracts stock monthly returns df from dictionary, `dic`, and left merge it with
    a DataFrame containing values of stock characteristics, 'df_cha'. Then, it shifts
    all the characteristics columns 1 month forward.
    The results table has a Monthly frequency PeriodIndex, containing rows for each
    year-month that include the returns for that period and the characteristics
    from the previous year-month for each stock.

    Parameters
    ----------
    ret : dict
        A dictionary containing two items, where each item is a DataFrame that provides daily and monthly returns.
        See the docstring of the `aj_ret_dict` function in etl.py for a description of this dictionary.
    df_cha : df
        A DataFrame containing calculated characteristics for stocks, total volatility here.
        See the docstring of the `vol_cal` function in this script for a description of this dataframe.
    cha_name  :  str
        It is the name of the characteristic being calculated.
        Set it as 'vol' when calculating total volatility.

    Returns
    -------
    df
        A merged DataFrame with a Monthly frequency PeriodIndex, containing rows for each year-month that
        include the stock returns for that period and the characteristics from the previous year-month.
        - df.columns: All columns in the monthly return dataframe within `ret` and characteristics table `df_cha`.

        - df.index: Monthly frequency PeriodIndex with name of 'Year_Month'.
          It contains all PeriodIndex year-month of the monthly returns data frame.

    Examples:
    Note: The examples below are for illustration purposes. Your ticker/sample
    period may be different.


    >> ret_dict = etl._test_aj_ret_dict(tickers=['AAPL', 'TSLA'], start='2010-05-15', end='2010-08-31')
    >> _test_merge_tables(ret_dict, 'vol', ['Daily',])

        ----------------------------------------
       Monthly return table:
                      aapl      tsla
       Year_Month
       2010-06   -0.020827       NaN
       2010-07    0.022741 -0.163240
       2010-08   -0.055005 -0.023069
       Characteristic table:
                  aapl_vol  tsla_vol
       Year_Month
       2010-06     0.019396        NaN
       2010-07     0.015031   0.065355
       2010-08     0.012806   0.033770
       This means `df_m = merge_tables(ret_dic, df_cha, cha_name)
       The value of `df_m` is
                    aapl      tsla  aapl_vol  tsla_vol
       Date
       2010-06 -0.020827       NaN        NaN        NaN
       2010-07  0.022741 -0.163240   0.019396        NaN
       2010-08 -0.055005 -0.023069   0.015031   0.065355
       ----------------------------------------

    Hints:
     -----
     - when you use dataframes in the return dictionary, use copy() method to create a new object
       ensuring that modifications to the copied DataFrame do not affect the original DataFrame stored in the dictionary
     - Read shift() documentations to understand how to shift the values of a DataFrame along a specified axis
    """
    # <COMPLETE THIS PART>


# ------------------------------------------------------------------------------------
# Part 5.2: Read the cha_main function and understand the workflow in this script
# ------------------------------------------------------------------------------------
def cha_main(ret, cha_name, ret_freq_use: list):
    """Function to show work flow. This script is to calculate stock total volatility
       using daily return table and merge it with monthly return table.

    This function performs a few steps to construct characteristics:
    1. Call `vol_input_sanity_check` function to check the sanity of inputs to ensure
       they meet required formats and constraints.
    2. Call `vol_cal` function to calculate the stock characteristics.
    3. Call `merge_tables` function to merge step 2 output and monthly return table together

    Parameters
    ----------
    ret : dict
        A dictionary containing two items, where each item is a DataFrame that provides daily and monthly returns.
        See the docstring of the `aj_ret_dict` function in zid_project2_etl.py for a description of this dictionary.

    cha_name  :  str
        The name of the characteristic being calculated. In this project we will only calculate stock total volatility.
        So, set this parameter as 'vol', the short name for total volatility here.

    ret_freq_use  :  list
        It identifies that which frequency returns you will use in this function.
        Set it as ['Daily',] when calculating stock total volatility here.

    Returns
    -------
    df
        A merged DataFrame with a Monthly frequency PeriodIndex, containing rows for each year-month that
        include the stock monthly returns for that period and the characteristics, i.e., total volatility,
        from the previous year-month.
        - df.columns: All columns in the monthly return dataframe within `ret` dictionary generated from
          etl script and characteristics table, `df_cha`, generated from vol_cal function.
        - df.index: Monthly frequency PeriodIndex with name of 'Year_Month'.
          It contains all PeriodIndex year-month of the monthly returns data frame.

    Raises
    -------
        - Custom exceptions or errors if the sanity check fails or if any part of the characteristic calculation
          or merging process encounters issues.

    Note:
        The function assumes that `vol_input_sanity_check`, `vol_cal`, and `merge_tables` are defined elsewhere
        in the module with appropriate logic to handle the inputs and outputs as described.
    """
    # <COMPLETE THIS PART>


def _test_ret_dict_gen():
    """ Function for generating made-up dictionary output from etl.py.
        Update the made-up dictionary as necessary when testing functions.
    """

    idx = pd.to_datetime([
        '2019-01-28', '2019-01-29', '2019-01-30', '2019-01-31', '2019-02-01',
        '2019-02-05', '2019-02-06', '2019-02-07', '2019-02-08', '2019-02-11',
        '2019-02-12', '2019-02-13', '2019-02-14', '2019-02-15', '2019-02-18',
        '2019-02-19', '2019-02-20', '2019-02-21', '2019-02-22', '2019-02-25',
        '2019-02-26', '2019-02-27', '2019-02-28', '2019-03-01', '2019-03-02',
    ])

    stock1 = [
         0.023969,  0.005083, -0.021728, -0.036492,  0.002642,
         0.013220, 0.014490, -0.045329, 0.024182, 0.009146,
         -0.020552,  0.029547,  0.011807, -0.036482,  0.010892,
         -0.021478, -0.041856,  0.031371,  0.031062, -0.023821,
         0.023912,  0.018807,  0.036614,  0.028173, -0.039111,
    ]

    stock2 = [
          np.nan, np.nan, np.nan, np.nan, np.nan,
          np.nan, np.nan, np.nan, np.nan, np.nan,
          0.017068, -0.000414, -0.036619, -0.025764,  0.019535,
          0.019739,  0.037371, -0.011854, -0.017300, -0.023779,
          -0.036719, -0.043338, -0.04288, -0.009428,  0.010881,
    ]

    daily_ret_df = pd.DataFrame({'stock1': stock1, 'stock2': stock2, }, index=idx)
    daily_ret_df.index.name = 'Date'

    idx_m = pd.to_datetime(['2019-02-28', ]).to_period('M')
    stock1_m = [0.063590, ]
    stock2_m = [np.nan, ]
    monthly_ret_df = pd.DataFrame({'stock1': stock1_m, 'stock2': stock2_m, }, index=idx_m)
    monthly_ret_df.index.name = 'Year_Month'

    ret = {"Daily": daily_ret_df, "Monthly": monthly_ret_df}

    return ret


def _test_vol_input_sanity_check(ret, cha_name,  ret_freq_use):
    """ Test function for `vol_input_sanity_check`
    """
    vol_input_sanity_check(ret, cha_name,  ret_freq_use)


def _test_vol_cal(ret, cha_name,  ret_freq_use):
    """ Test function for `vol_cal`
    Examples:
    Note: The examples below are for illustration purposes.

    >> made_up_ret_dict = _test_ret_dict_gen()
    >> _test_vol_cal(made_up_ret_dict, cha_name, ret_freq_use)

        ----------------------------------------
        This means `df_cha = vol_cal(ret, cha_name, ret_freq_use)`, print out df_cha:

                    stock1_vol  stock2_vol
        Year_Month
        2019-02       0.026615         NaN

        Obj type is: <class 'pandas.core.frame.DataFrame'>

        <class 'pandas.core.frame.DataFrame'>
        PeriodIndex: 1 entries, 2019-02 to 2019-02
        Freq: M
        Data columns (total 2 columns):
         #   Column      Non-Null Count  Dtype
        ---  ------      --------------  -----
         0   stock1_vol  1 non-null      float64
         1   stock2_vol  0 non-null      float64
        dtypes: float64(2)
        memory usage: 24.0 bytes
        ----------------------------------------
    """

    df_cha = vol_cal(ret, cha_name, ret_freq_use)
    msg = "This means `df_cha = vol_cal(ret, cha_name, ret_freq_use)`, print out df_cha:"
    util.test_print(df_cha, msg)


def _test_merge_tables(ret, cha_name, ret_freq_use):
    """ Test function for `merge_tables`
    Examples:
    Note: The examples below are for illustration purposes.

    >> made_up_ret_dict = _test_ret_dict_gen()
    >> _test_merge_tables(made_up_ret_dict, cha_name, ret_freq_use)
        ----------------------------------------
        Monthly return table:
                     stock1 stock2
        Year_Month
        2019-02     0.06359   NaN
        Characteristic table:
                    stock1_vol  stock2_vol
        Year_Month
        2019-02       0.026615         NaN
        This means `df_m = merge_tables(ret, df_cha, cha_name)
        The value of `df_m` is
                     stock1 stock2  stock1_vol  stock2_vol
        Year_Month
        2019-02     0.06359   NaN         NaN         NaN
        ----------------------------------------

    """
    df_cha = vol_cal(ret, cha_name, ret_freq_use)
    df_m = merge_tables(ret, df_cha, cha_name)
    to_print = [
        f"Monthly return table:\n{ret['Monthly']}",
        f"Characteristic table:\n{df_cha}",
        "This means `df_m = merge_tables(ret, df_cha, cha_name)",
        f"The value of `df_m` is \n{df_m}",
    ]
    util.test_print('\n'.join(to_print))


def _test_cha_main(ret, cha_name, ret_freq_use):
    """ Test function for `cha_main`
    """
    df_cha_f = cha_main(ret, cha_name, ret_freq_use)
    msg = ("This means `df_cha_f = cha_main(ret, cha_name, ret_freq_use)`,\
            \nprint out df_cha_f:")
    util.test_print(df_cha_f, msg)

    return df_cha_f


if __name__ == "__main__":
    pass

    # use made-up return dictionary, _test_ret_dic_gen, to test functions:
    # made_up_ret_dict = _test_ret_dict_gen()
    # _test_vol_input_sanity_check(made_up_ret_dict, 'vol', ['Daily',])
    # _test_vol_cal(made_up_ret_dict, 'vol', ['Daily',])
    # _test_merge_tables(made_up_ret_dict, 'vol', ['Daily',])
    # _test_cha_main(made_up_ret_dict, 'vol', ['Daily',])

    # use test return dictionary generated by _test_aj_ret_dict to test functions:
    # ret_dict = etl._test_aj_ret_dict(tickers=['AAPL', 'TSLA'], start='2010-05-15', end='2010-08-31')
    # _test_vol_input_sanity_check(ret_dict, 'vol', ['Daily',])
    # _test_vol_cal(ret_dict, 'vol', ['Daily',])
    # _test_merge_tables(ret_dict, 'vol', ['Daily',])
    # _test_cha_main(ret_dict, 'vol', ['Daily',])

