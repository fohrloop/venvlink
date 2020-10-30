import argparse
import os 
from pathlib import Path 

from venvlink import VenvLink

parser = argparse.ArgumentParser(prog='venvlink', description='venvlink')
parser.add_argument('-d', '--delete', 
        help='Delete the virtual environment associated with project_name (instead of creating)',
        action="store_true", default=False,
)
parser.add_argument('-S', '--system-site-packages', 
    help='Give the virtual environment access to the system site-packages dir.',
    action="store_true",
    default=False,
)
parser.add_argument('projectname', action="store")

# Executed with "python -m venvlink [params]"
if __name__ == '__main__':
    args = parser.parse_args()

    vlink = VenvLink()

    if not args.delete:
        print(f'Creating venv for "{args.projectname}"')
        vlink.create_venv(args.projectname, workdir=Path(os.getcwd()), system_site_packages = args.system_site_packages)
    else:
        print(f'Deleting venv for "{args.projectname}"')
        vlink.delete_env(args.projectname)