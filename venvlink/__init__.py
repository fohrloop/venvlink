import logging 
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

import os 
from pathlib import Path
import subprocess
import sys 
import shutil 

from venvlink.__version__ import __version__
from venvlink.config import Configuration



logger = logging.getLogger(__name__)


def get_scripts_dir(venv_dir):
    """
    Parameters
    ---------
    venv_dir: pathlib.Path
        The virtual environment root dir.
    """
    return venv_dir / 'Scripts'

def get_from_scripts_dir(venv_dir, file='activate'):
    return get_scripts_dir(venv_dir) / file

def get_from_venv_dir(venv_dir, file='pyvenv.cfg'):
    return venv_dir / file

def get_venvlink_text(venv_project):
    text = f'The virtual environment is located at {venv_project}' + os.linesep
    text += f'Created with venvlink v.{__version__}'
    return text

class VenvLink:

    def __init__(self, config_file=None):
        config_file = Path(config_file) \
                      if config_file is not None else None
        self.config = Configuration(config_file) 

    def delete_env(self, project_name):
        """
        Removes virtual environment created with create_env.

        Parameters
        ----------
        project_name: str
            The project name for which the virtual enviroment
            was created. This should be the virtual environment 
            name in the folder where all the virtual environments
            are located.
        """

        folder = self.venv_folder / project_name
        if folder.exists():
            logger.info('Removing %s', folder)
    
            shutil.rmtree(folder)
        else:
            logger.info('Could not remove %s! No such folder.', folder)


    def create_venv(self, project_name, workdir, system_site_packages=False):
        """
        Parameters
        ----------
        project_name: str
            The project name for which the virtual enviroment
            is created. This will be the virtual environment 
            name in the folder where all the virtual environments
            are located.
        workdir: pathlib.Path
            The working directory; the directory into 
            which the "linked virtual environment" is created
            (with hardlinked Scripts/activate).
        system_site_packages: bool
            The --system_site_packages of "python -m venv"
        """

        # Create the virtual environment in the "centralized location"
        self._create_venv_to_venv_folder(project_name, system_site_packages=system_site_packages)

        # Create the virtual environment in the workdir, with hardlinks
        self._create_venv_to_workdir(workdir, project_name)


    def _create_venv_to_venv_folder(self, project_name, system_site_packages=False):

        # Create the folder for all the virtual environments
        self.venv_folder.mkdir(exist_ok=True, parents=True)

        self._check_that_venv_does_not_exist(project_name)
        subprocess_cmd = [sys.executable, '-m', 'venv', project_name]
        if system_site_packages:
            subprocess_cmd.append('--system-site-packages')
        logger.info('Running: %s with cwd=%s', subprocess_cmd, self.venv_folder)
        subprocess.run(subprocess_cmd, cwd=self.venv_folder)

    def _check_that_venv_does_not_exist(self, project_name):

        if not (self.venv_folder / project_name).exists():
            return # all ok.

        raise NotImplementedError('You can not make two projects to use the same venv (yet)')


    def _create_venv_to_workdir(self, workdir, project_name, venvname='venv'):
        # Create the working directory if it does not
        # exists (should probably always exist, but anyway.)
        workdir.mkdir(exist_ok=True, parents=True)
        
        venvdir_dst = workdir / venvname
        if venvdir_dst.exists():
            raise Exception(f'The {venvdir_dst} exists already! Remove it and try again!')

        venvdir_dst.mkdir()
        
        # Make hard links to needed files
        venvdir_src = self.venv_folder / project_name

        files_and_funcs = [
            ('pyvenv.cfg', get_from_venv_dir),
        ]
        for file in get_scripts_dir(venvdir_src).glob('*'):
            if file.is_file():
                files_and_funcs.append((file.name, get_from_scripts_dir))

        for file, func in files_and_funcs:
            file_src = func(venvdir_src, file)
            file_dst = func(venvdir_dst, file)
            file_dst.parent.mkdir(exist_ok=True, parents=True)
            """
            Compability of os.link:

            Changed in version 3.2: Added Windows support.
            New in version 3.3: Added the src_dir_fd, dst_dir_fd, and follow_symlinks arguments.
            Changed in version 3.6: Accepts a path-like object for src and dst.
            """
            # Creates a hard link from src to dst

            os.link(file_src, file_dst)

        with open(venvdir_dst / 'venvlink', 'w') as f:
            print(get_venvlink_text(venvdir_src), file=f)
    
    @property
    def venv_folder(self):
        return Path(self.config.venv_folder)

