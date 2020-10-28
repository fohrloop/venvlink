import os
from pathlib import Path 
import sys 

from venvlink.__version__ import __version__


def get_user_folder():
    if is_windows():
        return Path(os.environ['USERPROFILE'])
    else:
        NotImplementedError(f'venvlink v. {__version__} supports only Windows')


def is_windows():
    return sys.platform.startswith('win')


def get_venvlink_text(venv_project):
    text = 'The virtual environment is located at {venv_project}' + os.linesep*2
    text += f'Created with venvlink v.{__version__}'
    return text