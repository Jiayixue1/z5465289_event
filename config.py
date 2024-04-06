""" config.py

Configuration options for the project2 package         

"""
# IMPORTANT: Please do NOT modify this file

import os
import toolkit_config as tcfg


ROOTDIR = os.path.join(tcfg.PRJDIR, 'project2')
DATADIR = os.path.join(ROOTDIR, 'data')
# FF_CSV = os.path.join(DATADIR, 'ff_daily.csv')

TICMAP = {
        'AAL'    : 'American Airlines Group Inc',
        'AAPL'   : 'Apple Inc.',
        'ABBV'   : 'AbbVie Inc.',
        'BABA'   : 'Alibaba Group Holding Limited',
        'BAC'    : 'Bank of America Corporation',
        'CSCO'   : 'Cisco Systems, Inc.',
        'DAL'    : 'Delta Air Lines, Inc.',
        'DIS'    : 'The Walt Disney Company',
        'FB'     : 'Facebook, Inc.',
        'GE'     : 'General Electric Company',
        'INTC'   : 'Intel Corporation',
        'JNJ'    : 'Johnson & Johnson',
        'KO'     : 'The Coca-Cola Company',
        'MSFT'   : 'Microsoft Corporation',
        'NVDA'   : 'NVIDIA Corporation',
        'ORCL'   : 'Oracle Corporation',
        'PFE'    : 'Pfizer Inc.',
        'PG'     : 'The Procter & Gamble Company',
        'PYPL'   : 'PayPal Holdings, Inc.',
        'T'      : 'AT&T Inc. (T)',
        'TSLA'   : 'Tesla, Inc.',
        'TSM'    : 'Taiwan Semiconductor Manufacturing Company Limited',
        'V'      : 'Visa Inc.',
        }
TICKERS = sorted(TICMAP.keys())
    
# -------------------------------------------------------- 
#   Aux function to process col names
# --------------------------------------------------------
def standardise_colnames(df):
    """ Renames the columns in `df` so that 
    - Names are lower case
    - Spaces are replaced with '_'

    Parameters
    ----------
    df : dataframe


    Notes
    -----
    - If column with the standardised name already exists, the new column will
      include a '_' prefix

    Examples
    -------

    >> df = pd.DataFrame([(1, 2), (3, 4)], columns=['A', 'B C'])
    >> print(df)

       A  B C
    0  1    2
    1  3    4

    >> df2 = standardise_colnames(df)
    >> print(df2)

       a  b_c
    0  1    2
    1  3    4

    """
    cols = set(df.columns)
    # You can define `local` functions
    def _parse_name(colname):
        # Processes the column name
        new_name = colname.lower().replace(' ', '_')
        # Decide what to do. The options are:
        # 1) column name is already properly formatted:
        #   => do nothing
        # 2) column name is not properly formatted but exists in the dataframe
        #   => Include '_' prefix
        # 3) Else: return formatted name
        if new_name == colname: 
            # Returns original column
            return colname
        elif new_name in cols:
            return '_' + new_name
        else:
            return new_name
    return df.rename(columns=_parse_name)



