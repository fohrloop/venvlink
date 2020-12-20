from configparser import ConfigParser
from functools import partial
import io
import logging
import os
from pathlib import Path

from venvlink.utils import get_user_folder, is_windows, is_in_accepted_values, get_input
from venvlink.exceptions import ImproperlyConfiguredError


def get_venvlinkrc():
    """
    Returns
    -------
    venvlinkrc: pathlib.Path
        The path to .venvlinkrc file.
        (the file might not exist)
    """
    filename = ".venvlinkrc"
    venvlinkrc = get_user_folder() / filename
    return venvlinkrc


def is_valid_path_or_empty(x):
    x = x.strip()
    if not x:  # empty string
        return True
    try:
        path = Path(x)
    except Exception:
        return False
    if not path.is_absolute():
        return False
    return True


def get_default_config(interactive=False):
    default_venv_folder = str(get_user_folder() / "venvs")

    text = "Folder for saving virtual envs?"
    text += f" [Default: {default_venv_folder}]" + os.linesep

    value = get_input(text, is_valid_path_or_empty).strip()
    if value:
        default_venv_folder = value

    default_config = """
    [general]
    VENV_FOLDER = {DEFAULT_VENV_FOLDER}
    """.strip().format(
        DEFAULT_VENV_FOLDER=default_venv_folder
    )
    return default_config


def init_config():
    file = get_venvlinkrc()
    if file.exists():

        text = f"WARNING: The configuration file '{file}' for venvlink exists already. "
        text += f"If you continue, the existing file will be OVERRIDDEN "
        text += "with the default configuration file " + os.linesep
        print(text)
        question = "Override current configuration file with a new one?"

        value = None
        while value not in {"Y", "N"}:
            print(question)
            prompt = "[Y] Yes [N] No [S] Show current .venlinkrc\n"
            validator = partial(is_in_accepted_values, accepted_values={"Y", "N", "S"})
            value = get_input(prompt, validator).upper()
            if value == "S":
                print(f"\nCurrent configuration ({file}):")
                print("-" * 28)
                with open(file) as f:
                    print(f.read())

        if value == "N":
            print("Canceled.")
            return

    config = create_default_config()

    save_config_to_file(config, file)
    print("Saved default config to file:", file)


def create_default_config():
    config = ConfigParser()
    buf = io.StringIO(get_default_config())
    config.read_file(buf)
    return config


def save_config_to_file(config, file):
    with open(file, "w", encoding="utf-8") as f:
        config.write(f)


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

    def load_config(self):
        config = ConfigParser()
        try:
            with open(self.file, encoding="utf-8") as f:
                config.read_file(f)

        except FileNotFoundError:
            logging.debug(
                "Configuration file for venvlink does not exist. Using default configuration, instead"
            )
            config = create_default_config()
            self.save_config(config)
        return config

    def save_config(self, config):
        logging.info("Saving %s", self.file)
        save_config_to_file(config, self.file)

    @property
    def venv_folder(self):
        return self.get_key(section="general", key="venv_folder")

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
            raise ImproperlyConfiguredError(
                self._get_improperly_configured_error_text(section, key)
            )

        if strip_quotes:
            val = val.strip('"').strip("'")

        return val

    def _get_improperly_configured_error_text(self, section, key):
        text = f'The section "{section}" of {self.file} did not contain key "{key}"'
        text += os.linesep * 2
        text += f"To fix this, ensure that {self.file} contains" + os.linesep * 2
        text += f"[{section}]" + os.linesep
        text += f"{key} = <some_value>" + os.linesep
        return text
