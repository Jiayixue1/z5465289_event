import os
import config as cfg
import pandas as pd


# This is an auxiliary function, please do not modify
COLOR_CODE = {
    'Red': '\033[91m',
    'Green': '\033[92m',
    'Blue': '\033[94m',
    'Cyan': '\033[96m',
    'White': '\033[97m',
    'Yellow': '\033[93m',
    'Magenta': '\033[95m',
    'Black ': '\033[90m',
    }

def test_print(obj, msg=None):
    """ Pretty prints `obj`. Will be used by other `_test` functions

    Parameters
    ----------
    obj : any object

    msg : str, optional
        Message preceding obj representation

    """
    import pprint as pp
    sep = '-' * 40
    if isinstance(obj, str):
        prt = obj
    else:
        prt = pp.pformat(obj)
        prt = f'{prt}\n\nObj type is: {type(obj)}'
    if msg is not None:
        prt = f'{msg}\n\n{prt}'
    to_print = [
        '',
        sep,
        prt,
    ]
    print('\n'.join(to_print))
    if isinstance(obj, pd.DataFrame):
        print('')
        obj.info()
    if isinstance(obj, pd.Series):
        print('')
        obj.info()
    if isinstance(obj, dict):
        for k, i in obj.items():
            if isinstance(i, pd.DataFrame) or isinstance(i, pd.Series):
                print(f'\nthe Key of the dictionary is {k}, value info:')
                i.info()
            else:
                print('')

    print(sep)


# This is an auxiliary function, please do not modify
def test_cfg():
    """ This test function will help you determine if the config.py module inside
    the project2 package was successfully imported as `cfg` and if the files
    are where they should be:

    toolkit/
    |
    |__ project2/
    |   |__ data/       <-- project2.config.DATADIR
    |
    """
    # Test if the data folder is inside the project2 folder
    # NOTE: The "parent" of the `data` folder is `project2`
    parent = os.path.dirname(cfg.DATADIR)
    to_print = f'''
The variable `parent` should point to the project2 folder:
  parent: '{parent}'
  Folder exists: '{os.path.exists(parent)}'

The data folder for this project is located at:
  cfg.DATADIR: '{cfg.DATADIR}'
  Folder exists: '{os.path.exists(cfg.DATADIR)}'
'''
    print(to_print.strip())


def color_print(msg, color=None):
    """ This function will help you print an obj in different colors.
        As default, it will print obj with Green color.
        If color parameter is specified, it will extract color escape code from COLOR_CODE to complete the task.
    """

    if color:
        color_code = COLOR_CODE[color]
        print(f'{color_code}{msg}\033[0m')
    else:
        color_code = COLOR_CODE['Green']
        print(f'{color_code}{msg}\033[0m')
