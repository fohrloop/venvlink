import logging 
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

from functools import partial 
import os 
from pathlib import Path
import subprocess
import sys 
import shutil 

from venvlink.__version__ import __version__
from venvlink.config import Configuration
from venvlink.exceptions import UserAborted
from venvlink.utils import is_in_accepted_values, get_input

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
        system_site_packages: bool
            The --system_site_packages of "python -m venv"
        """

        try:
            self._check_no_venv_in_workdir(workdir, project_name)
        except UserAborted:
            print('Canceled.')
            return 

        try:
            # Create the virtual environment in the "centralized location"
            self._create_venv_to_venv_folder(project_name, system_site_packages=system_site_packages)
        except UserAborted:
            print('Canceled.')
            return 

        # Create the "proxied" virtual environment in the workdir
        self._create_venv_to_workdir(workdir, project_name)


    def _create_venv_to_venv_folder(self, project_name, system_site_packages=False):

        # Create the folder for all the virtual environments
        self.venv_folder.mkdir(exist_ok=True, parents=True)

        ret = self._check_that_venv_does_not_exist(project_name)

        if ret == 'skipcreate':
            return 
        if ret == 'newname':
            project_name = self._get_new_venv_name()

        subprocess_cmd = [sys.executable, '-m', 'venv', project_name]
        if system_site_packages:
            subprocess_cmd.append('--system-site-packages')
        logger.info('Running: %s with cwd=%s', subprocess_cmd, self.venv_folder)
        subprocess.run(subprocess_cmd, cwd=self.venv_folder)

    def __venv_exists(self, project_name):
        return (self.venv_folder / project_name).exists()

    def _check_that_venv_does_not_exist(self, project_name):
        """
        Returns
        ret: str
            'continue' 'skipcreate' or 'newname'
        """
        if not self.__venv_exists(project_name):
            return 'continue'

        return self._when_venv_exists_already(project_name)

    def _get_new_venv_name(self):

        prompt =  'Give a new projectname: '
        errortxt = 'Sorry, that projectname exists already. '
        return get_input(prompt, validator=lambda x: not self.__venv_exists(x), on_validationerror=errortxt)

    def _when_venv_exists_already(self, project_name):
        """
        When venv already exists with the project_name, ask
        user opinion.

        Returns
        -------
        ret: str
            'skipcreate' or 'newname'

        Raises
        ------
        UserAborted, if user aborted.

        """
        text = f'The virtual environment for a projectname "{project_name}" exists already. '
        text += f'If you use the name "{project_name}", you will SHARE the virtual environment '
        text += 'with the other project(s) using the same name.' + os.linesep
        text += 'Continue?' + os.linesep
        print(text)

        prompt =  '[Y] Yes [N] No, give new name. [A] Abort: '
        validator = partial(is_in_accepted_values, accepted_values={'Y', 'N', 'A'})
        value = get_input(prompt, validator).upper()

        if value == 'Y':
            return 'skipcreate'
        elif value == 'N':
            return 'newname'
        elif value == 'A':
            raise UserAborted()
    

    def _check_no_venv_in_workdir(self, workdir, project_name, venvname='venv'):
            
        venvdir_dst = workdir / venvname
        if venvdir_dst.exists():
            print(f'The {venvdir_dst} exists already!')
            print('Do you want to remove it?')

            prompt =  '[Y] Yes [A] Abort: '
            validator = partial(is_in_accepted_values, accepted_values={'Y', 'A'})
            value = get_input(prompt, validator).upper()
            
            if value == 'A':
                raise UserAborted()
            elif value == 'Y':
                print('Removing ', str(venvdir_dst))
                shutil.rmtree(venvdir_dst)
            else: # should not ever happen.
                ValueError()

        return True 

    def _create_venv_to_workdir(self, workdir, project_name, venvname='venv'):
        # Create the working directory if it does not
        # exists (should probably always exist, but anyway.)
        workdir.mkdir(exist_ok=True, parents=True)
        
        venvdir_dst = workdir / venvname

        venvdir_dst.mkdir()
        
        # Make proxies to needed files
        venvdir_src = self.venv_folder / project_name

        
        contents = (   
            ( 'Scripts' + os.path.sep  + 'Activate.ps1', f"""Write-Output 'venvlink: Activating virtual env in "{venvdir_src}"'
                & \"{venvdir_src / 'Scripts' /'Activate.ps1' }\""""),
        )

        for file, content in contents:
            file_dst = venvdir_dst / file
            file_dst.parent.mkdir(exist_ok=True, parents=True)
            with open(file_dst, 'w', encoding='utf-8') as f:
                print(content, file=f)


        with open(venvdir_dst / 'venvlink', 'w') as f:
            print(get_venvlink_text(venvdir_src), file=f)
    
    @property
    def venv_folder(self):
        return Path(self.config.venv_folder)

