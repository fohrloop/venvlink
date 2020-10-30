import os 
from pathlib import Path 
import shutil 

from venvlink import VenvLink

folder = Path(__file__).resolve().parent / 'test_data'


def test_vlink():
    venvlinkrc = folder / '.venvlinkrc'
    venv_folder = folder / 'venvs'
    vlink = VenvLink(venvlinkrc)

    # Test that configuration is read correctly
    assert str(vlink.venv_folder) == r'C:\some-folder'

    # Change configuration so the test will use test_data folder
    vlink.config.config['general']['venv_folder'] = str(venv_folder)
    assert str(vlink.venv_folder) == str(venv_folder)

    # Set working directory
    workdir = folder / 'some' / 'path' / 'there' / 'workdir'
    workdir.mkdir(exist_ok=True, parents=True)
    os.chdir(workdir)

    # Create new virtual environment.
    new_venv_dir = workdir / 'venv'
    if new_venv_dir.exists():
        shutil.rmtree(new_venv_dir)
    if vlink.venv_folder.exists():
        shutil.rmtree(vlink.venv_folder)
    assert not new_venv_dir.exists()
    assert not vlink.venv_folder.exists()
    vlink.create_venv("testing", workdir=workdir)
    assert vlink.venv_folder.exists()
    venv_project = vlink.venv_folder / 'testing'
    assert new_venv_dir.exists()
    assert venv_project.exists()

    activate_src = venv_project / 'Scripts' / 'Activate.ps1'
    activate_dst = new_venv_dir / 'Scripts' / 'Activate.ps1'

    assert activate_src.exists()
    assert activate_dst.exists()


    vlink.delete_env("testing")
    assert not venv_project.exists()
    # cleanup
    os.chdir(folder)
    shutil.rmtree(folder / 'some') 
    shutil.rmtree(venv_folder) 


if __name__ == '__main__':
    test_vlink()