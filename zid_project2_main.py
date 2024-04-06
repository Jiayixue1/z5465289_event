""" zid_project2_main.py

"""
# ----------------------------------------------------------------------------
# Part 1: Read the documentation for the following methods:
#   – pandas.DataFrame.mean
#   - pandas.Series.concat
#   – pandas.Series.count
#   – pandas.Series.dropna
#   - pandas.Series.index.to_period
#   – pandas.Series.prod
#   – pandas.Series.resample
#   - ......
# Hint: you can utilize modules covered in our lectures, listed above and any others.
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Part 2: import modules inside the project2 package
# ----------------------------------------------------------------------------
# Create import statements so that the module config.py and util.py (inside the project2 package)
# are imported as "cfg", and "util"
#
# <COMPLETE THIS PART>


# We've imported other needed scripts and defined aliases. Please keep using the same aliases for them in this project.
import zid_project2_etl as etl
import zid_project2_characteristics as cha
import zid_project2_portfolio as pf

import pandas as pd


# -----------------------------------------------------------------------------------------------
# Part 3: Follow the workflow in portfolio_main function
#         to understand how this project construct total volatility long-short portfolio
# -----------------------------------------------------------------------------------------------
def portfolio_main(tickers, start, end, cha_name, ret_freq_use, q):
    """
    Constructs equal-weighted portfolios based on the specified characteristic and quantile threshold.
    We focus on total volatility investment strategy in this project 2.
    We name the characteristic as 'vol'

    This function performs several steps to construct portfolios:
    1. Call `aj_ret_dict` function from etl script to generate a dictionary containing daily and
       monthly returns.
    2. Call `cha_main` function from cha script to generate a DataFrame containing stocks' monthly return
       and characteristic, i.e., total volatility, info.
    3. Call `pf_main` function from pf script to construct a DataFrame with
       equal-weighted quantile and long-short portfolio return series.

    Parameters
    ----------
    tickers : list
        A list including all tickers (can include lowercase and/or uppercase characters) in the investment universe

    start  :  str
        The inclusive start date for the date range of the price table imported from data folder
        For example: if you enter '2010-09-02', function in etl script will include price
        data of stocks from this date onwards.
        And make sure the provided start date is a valid calendar date.

    end  :  str
        The inclusive end date for the date range, which determines the final date
        included in the price table imported from data folder
        For example: if you enter '2010-12-20', function in etl script will encompass data
        up to and including December 20, 2010.
        And make sure the provided start date is a valid calendar date.

    cha_name : str
        The name of the characteristic. Here, it should be 'vol'

    ret_freq_use  :  list
        It identifies that which frequency returns you will use to construct the `cha_name`
        in zid_project2_characteristics.py.
        Set it as ['Daily',] when calculating stock total volatility here.

    q : int
        The number of quantiles to divide the stocks into based on their characteristic values.


    Returns
    -------
    dict_ret : dict
        A dictionary with two items, each containing a dataframe of daily and monthly returns
        for all stocks listed in the 'tickers' list.
        This dictionary is the output of `aj_ret_dict` in etl script.
        See the docstring there for a description of it.

    df_cha : df
        A DataFrame with a Monthly frequency PeriodIndex, containing rows for each year-month
        that include the stocks' monthly returns for that period and the characteristics,
        i.e., total volatility, from the previous year-month.
        This df is the output of `cha_main` function in cha script.
        See the docstring there for a description of it.

    df_portfolios : df
        A DataFrame containing the constructed equal-weighted quantile and long-short portfolios.
        This df is the output of `pf_cal` function in pf script.
        See the docstring there for a description of it.

    """

    # --------------------------------------------------------------------------------------------------------
    # Part 4: Complete etl scaffold to generate returns dictionary and to make ad_ret_dic function works
    # --------------------------------------------------------------------------------------------------------
    dict_ret = etl.aj_ret_dict(tickers, start, end)

    # ---------------------------------------------------------------------------------------------------------
    # Part 5: Complete cha scaffold to generate dataframe containing monthly total volatility for each stock
    #         and to make char_main function work
    # ---------------------------------------------------------------------------------------------------------
    df_cha = cha.cha_main(dict_ret, cha_name,  ret_freq_use)

    # -----------------------------------------------------------------------------------------------------------
    # Part 6: Read and understand functions in pf scaffold. You will need to utilize functions there to
    #         complete some of the questions in Part 7
    # -----------------------------------------------------------------------------------------------------------
    df_portfolios = pf.pf_main(df_cha, cha_name, q)

    util.color_print('Portfolio Construction All Done!')

    return dict_ret, df_cha, df_portfolios


# ----------------------------------------------------------------------------
# Part 7: Complete the auxiliary functions
# ----------------------------------------------------------------------------
def get_avg(df: pd.DataFrame, year):
    """ Returns the average value of all columns in the given df for a specified year.

    This function will calculate the column average for all columns
    from a data frame `df`, for a given year `year`.
    The data frame `df` must have a DatetimeIndex or PeriodIndex index.

    Missing values will not be included in the calculation.

    Parameters
    ----------
    df : data frame
        A Pandas data frame with a DatetimeIndex or PeriodIndex index.

    year : int
        The year as a 4-digit integer.

    Returns
    -------
    ser
        A series with the average value of columns for the year `year`.

    Example
    -------
    For a data frame `df` containing the following information:

        |            | tic1 | tic2  |
        |------------+------+-------|
        | 1999-10-13 | -1   | NaN   |
        | 1999-10-14 | 1    | 0.032 |
        | 2020-10-15 | 0    | -0.02 |
        | 2020-10-16 | 1    | -0.02 |

        >> res = get_avg(df, 1999)
        >> print(res)
        tic1      0.000
        tic2      0.032
        dtype: float64

    """
    # <COMPLETE THIS PART>


def get_cumulative_ret(df):
    """ Returns cumulative returns for input DataFrame.

    Given a df with return series, this function will return the
    buy and hold return for the whole period.

    Parameters
    ----------
    df : DataFrame
        A Pandas DataFrame containing monthly portfolio returns
        with a PeriodIndex index.

    Returns
    -------
    df
        A df with the cumulative returns for portfolios, ignoring missing observations.

    Notes
    -----
    The buy and hold cumulative return will be computed as follows:

        (1 + r1) * (1 + r2) *....* (1 + rN) - 1
        where r1, ..., rN represents monthly returns

    """
    # <COMPLETE THIS PART>


# ----------------------------------------------------------------------------
# Part 8: Answer questions
# ----------------------------------------------------------------------------
# NOTES:
#
# - THE SCRIPTS YOU NEED TO SUBMIT ARE
#   zid_project2_main.py, zid_project2_etl.py, and zid_project2_characteristics.py
#
# - Do not create any other functions inside the scripts you need to submit unless
#   we ask you to do so.
#
# - For this part of the project, only the answers provided below will be
#   marked. You are free to create any function you want (IN A SEPARATE
#   MODULE outside the scripts you need to submit).
#
# - All your answers should be strings. If they represent a number, include 4
#   decimal places unless otherwise specified in the question description
#
# - Here is an example of how to answer the questions below. Consider the
#   following question:
#
#   Q0: Which ticker included in config.TICMAP starts with the letter "C"?
#   Q0_answer = '?'
#
#   You should replace the '?' with the correct answer:
#   Q0_answer = 'CSCO'
#
#
#     To answer the questions below, you need to run portfolio_main function in this script
#     with the following parameter values:
#     tickers: all tickers included in the dictionary config.TICMAP,
#     start: '2000-12-29',
#     end: '2021-08-31',
#     cha_name: 'vol'.
#     ret_freq_use: ['Daily',],
#     q: 3
#     Please name the three output files as DM_Ret_dict, Vol_Ret_mrg_df, EW_LS_pf_df.
#     You can utilize the three output files and auxiliary functions to answer the questions.


# Q1: Which stock in your sample has the lowest average daily return for the
#     year 2008 (ignoring missing values)? Your answer should include the
#     ticker for this stock.
#     Use the output dictionary, DM_Ret_dict, and auxiliary function in this script
#     to do the calculation.
Q1_ANSWER = '?'


# Q2: What is the daily average return of the stock in question 1 for the year 2008.
#     Use the output dictionary, DM_Ret_dict, and auxiliary function in this script
#     to do the calculation.
Q2_ANSWER = '?'


# Q3: Which stock in your sample has the highest average monthly return for the
#     year 2019 (ignoring missing values)? Your answer should include the
#     ticker for this stock.
#     Use the output dictionary, DM_Ret_dict, and auxiliary function in this script
#     to do the calculation.
Q3_ANSWER = '?'


# Q4: What is the average monthly return of the stock in question 3 for the year 2019.
#     Use the output dictionary, DM_Ret_dict, and auxiliary function in this script
#     to do the calculation.
Q4_ANSWER = '?'


# Q5: What is the average monthly total volatility for stock 'TSLA' in the year 2010?
#     Use the output dataframe, Vol_Ret_mrg_df, and auxiliary function in this script
#     to do the calculation.
Q5_ANSWER = '?'


# Q6: What is the ratio of the average monthly total volatility for stock 'V'
#     in the year 2008 to that in the year 2018? Keep 1 decimal places.
#     Use the output dataframe, Vol_Ret_mrg_df, and auxiliary function in this script
#     to do the calculation.
Q6_ANSWER = '?'


# Q7: How many effective year-month for stock 'TSLA' in year 2010. An effective year-month
#     row means both monthly return in 'tsla' column and total volatility in 'tsla_vol'
#     are not null.
#     Use the output dataframe, Vol_Ret_mrg_df, to do the calculation.
#     Answer should be an integer
Q7_ANSWER = '?'


# Q8: How many rows and columns in the EW_LS_pf_df data frame?
#     Answer should be two integer, the first represent number of rows and the two numbers need to be
#     separated by a comma.
Q8_ANSWER = '?'


# Q9: What is the average equal weighted portfolio return of the quantile with the
#     lowest total volatility for the year 2019?
#     Use the output dataframe, EW_LS_pf_d, and auxiliary function in this script
#     to do the calculation.
Q9_ANSWER = '?'


# Q10: What is the cumulative portfolio return of the total volatility long-short portfolio
#      over the whole sample period?
#      Use the output dataframe, EW_LS_pf_d, and auxiliary function in this script
#     to do the calculation.
Q10_ANSWER = '?'


# ----------------------------------------------------------------------------
# Part 9: Add t_stat function
# ----------------------------------------------------------------------------
# We've outputted EW_LS_pf_df file and save the total volatility long-short portfolio
# in 'ls' column from Part 8.

# Please add an auxiliary function called ‘t_stat’ below.
# You can design the function's parameters and output table.
# But make sure it can be used to output a DataFrame including three columns:
# 1.ls_bar, the mean of 'ls' columns in EW_LS_pf_df
# 2.ls_t, the t stat of 'ls' columns in EW_LS_pf_df
# 3.n_obs, the number of observations of 'ls' columns in EW_LS_pf_df

# Notes:
# Please add the function in zid_project2_main.py.
# The name of the function should be t_stat and including docstring.
# Please replace the '?' of ls_bar, ls_t and n_obs variables below
# with the respective values of the 'ls' column in EW_LS_pf_df from Part 8,
# keep 4 decimal places if it is not an integer:
ls_bar = '?'
ls_t = '?'
n_obs = '?'
# ls_bar = '0.0073'
# ls_t = '1.3847'
# n_obs = '235'


# <ADD THE t_stat FUNCTION HERE>


# ----------------------------------------------------------------------------
# Part 10: share your team's project 2 git log
# ----------------------------------------------------------------------------
# In week6 slides, we introduce Git and show how to work collaboratively on Git.
# You are not necessary to use your UNSW email to register the git account.
# But when you set up your username, you will follow the format zid...FirstNameLastName.
#
# Please follow the instruction there to work with your teammates. The team leader
# will need to create a Project 2 Repo on GitHub and grant teammates access to the Repo.
# For teammates, you will need to clone the repo and then coding as a team.
#
# The team will need to generate a git log from git terminal.
# You can use 'cd <...>' direct your terminal into the project 2 repo directory,
# then export the git log:
# git log --pretty=format:"%h%x09%an%x09%ad%x09%s" >teamX.txt
# Here is an example output:
# .......
# dae0fa9	zid1234 Sarah Xiao	Mon Feb 12 16:33:22 2024 +1100	commit and push test
# fa26a62	zid1234 Sarah Xiao	Mon Feb 12 16:32:02 2024 +1100	commit and push test
# 800bf27	zid5678 David Lee	Mon Feb 12 16:12:30 2024 +1100	for testing
# .......
#
# Please replace the """?""" with your team's project 2 git log:
git_log = """?"""

# ----------------------------------------------------------------------------
# Part 11: project 2 mini-presentation
# ----------------------------------------------------------------------------
# In this part, you are going to record and present a strictly less than 15 minutes long presentation.
# You should seek to briefly describe:
# 1.	What are the null and alternative hypotheses that the project 2 is testing
# 2.	What’s the methodology of the portfolio construction
#       and how is it implemented in Project 2 codebase?
# 3.	What inferences can we draw from the output of Part 9,
#       including the average return and t-stats of the long-short portfolio?
# 4.	Do you think the results are reliable? Why or why not?
# 5.	Is there any further work you would like to pursue based on Project 2?
#       Share your to-do list.
#
# For this mini-presentation, it is up to the group to decide whether all the members
# are in the presentation video or not.
# Please use Zoom to record it. The final submission should be a zoom recording link.

# Please replace the '?' with your team's presentation video zoom link:
Presentation_zoom_link = '?'
Password_of_your_video = '?'


def _test_get_avg():
    """ Test function for `get_avg`
    """
    # Made-up data
    ret = pd.Series({
        '2019-01-01': 1.0,
        '2019-01-02': 2.0,
        '2020-10-02': 4.0,
        '2020-11-12': 4.0,
    })
    df = pd.DataFrame({'some_tic': ret})
    df.index = pd.to_datetime(df.index)

    msg = 'This is the test data frame `df`:'
    util.test_print(df, msg)

    res = get_avg(df,  2019)
    to_print = [
        "This means `res =get_avg(df, year=2019) --> 1.5",
        f"The value of `res` is {res}",
    ]
    util.test_print('\n'.join(to_print))


def _test_get_cumulative_ret():
    """ Test function for `get_ann_ret`

    To construct this example, suppose first that holding the stock for 400
    trading days gives a total return of 1.5 (so 50% over 400 trading days).

    The annualised return will then be:

        (tot_ret)**(252/N) - 1 = 1.5 ** (252/400) - 1 = 0.2910

    Create an example data frame with 400 copies of the daily yield, where

        daily yield = 1.5 ** (1/400) - 1

    """
    # Made-up data
    idx_m = pd.to_datetime(['2019-02-28',
                            '2019-03-31',
                            '2019-04-30',]).to_period('M')
    stock1_m = [0.063590, 0.034290, 0.004290]
    stock2_m = [None, 0.024390, 0.022400]
    monthly_ret_df = pd.DataFrame({'stock1': stock1_m, 'stock2': stock2_m, }, index=idx_m)
    monthly_ret_df.index.name = 'Year_Month'
    msg = 'This is the test data frame `monthly_ret_df`:'
    util.test_print(monthly_ret_df, msg)

    res = get_cumulative_ret(monthly_ret_df)
    to_print = [
        "This means `res =get_cumulative_ret(monthly_ret_df)",
        f"The value of `res` is {res}",
    ]
    util.test_print('\n'.join(to_print))


if __name__ == "__main__":
    pass






