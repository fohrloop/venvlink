from configparser import ConfigParser
import io 
import logging 
import os 
from pathlib import Path 

from venvlink.utils import get_user_folder, is_windows
from venvlink.exceptions import ImproperlyConfiguredError

def get_venvlinkrc():
    filename = '.venvlinkrc'
    venvlinkrc = get_user_folder() / filename
    return venvlinkrc

def get_default_config():
    default_config = """
    [general]
    VENV_FOLDER = {DEFAULT_VENV_FOLDER}
    """.strip().format(
        DEFAULT_VENV_FOLDER=str(get_user_folder() / 'venvs'))
    return default_config


class Configuration:

    def __init__(self, file=None):
        """
        Parameters
        ----------
        file: None or pathlib.Path
            The path to the ".venvlinkrc" (the
            configuration file). 
        """
        self.file = get_venvlinkrc() if file is None else file

        self.config = self.load_config()


    def create_default_config(self):
        config = ConfigParser()
        buf = io.StringIO(get_default_config())
        config.read_file(buf)
        return config

    def load_config(self):
        config = ConfigParser()
        try:
            with open(self.file, encoding='utf-8') as f:
                config.read_file(f)

        except FileNotFoundError:
            logging.debug("Configuration file for venvlink does not exist. Using default configuration, instead")
            config = self.create_default_config()
            self.save_config(config)
        return config

    def save_config(self, config):
        logging.info("Configuration file for venvlink does not exist. Creating %s", self.file)
        with open(self.file, 'w', encoding='utf-8') as f:
            config.write(f)

    @property
    def venv_folder(self):
        return self.get_key(section='general', key='venv_folder')

    def get_key(self, section, key, strip_quotes=True):
        """
        Gets a key from a [section] from the venvlink
        configuration file.

        Parameters
        ----------
        section: str
            Name of the section.
        key: str
            Name of the key inside [section]
        strip_quotes: bool
            If True, drops single and double quotes from
            the both ends of the string.
        """
        try:
            val = self.config[section][key]
        except KeyError:
            raise ImproperlyConfiguredError(self._get_improperly_configured_error_text(section, key))
        
        if strip_quotes:
            val = val.strip('\"').strip("\'")

        return val 

    def _get_improperly_configured_error_text(self, section, key):
        text =  f'The section "{section}" of {self.file} did not contain key "{key}"'
        text += os.linesep*2
        text += f'To fix this, ensure that {self.file} contains' + os.linesep*2
        text += f'[{section}]' + os.linesep
        text += f'{key} = <some_value>' + os.linesep
        return text 

CONFIGURATION = Configuration()

