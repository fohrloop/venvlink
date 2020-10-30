import os
from pathlib import Path 
import sys 
from venvlink.__version__ import __version__


def is_in_accepted_values(value, accepted_values):
    """
    Case-insensitive check for accepted values

    Parameters
    ---------
    value: str
        The string to be validated
    accepted_values: str
        The accepted values. Use a set of UPPERCASE
        strings.
    """
    if value.upper() in accepted_values:
        return True
    return False


def get_input(prompt, validator, on_validationerror=None):
    """
    Parameters
    ----------
    prompt: str
        The text to show to user when asking for input
    validator: function
        The function to call, with the user input as argument
        * function should return True, if the input is ok
        * function should return False, if input is not ok
    on_validationerror: str
        The text to show if validation with `func` fails
    """
    while True:
        value = input(prompt)
        if validator(value):
            return value
        if on_validationerror:
            print(on_validationerror)



def get_user_folder():
    if is_windows():
        return Path(os.environ['USERPROFILE'])
    else:
        NotImplementedError(f'venvlink v. {__version__} supports only Windows')


def is_windows():
    return sys.platform.startswith('win')


