import argparse
import os
from pathlib import Path

from venvlink import VenvLink
from venvlink.config import init_config
from venvlink.__version__ import __version__

parser = argparse.ArgumentParser(prog="venvlink", description=f"venvlink {__version__}")

parser.add_argument(
    "--init",
    help="Initiate the venvlink configuration file (.venvlinkrc)",
    action="store_true",
    default=False,
)

parser.add_argument(
    "-d",
    "--delete",
    help="Delete the virtual environment associated with project_name (instead of creating)",
    action="store_true",
    default=False,
)
parser.add_argument(
    "-S",
    "--system-site-packages",
    help="Give the virtual environment access to the system site-packages dir.",
    action="store_true",
    default=False,
)
parser.add_argument("projectname", action="store", nargs="?")


def create_venv(args):
    if args.projectname is None:
        print(
            f'The positional argument "projectname" is required for creating a virtual environment!'
        )
        return
    print(f'Creating venv for "{args.projectname.strip()}"')
    vlink = VenvLink()
    vlink.create_venv(
        args.projectname.strip(),
        workdir=Path(os.getcwd()),
        system_site_packages=args.system_site_packages,
    )


def delete_env(args):
    if args.projectname is None:
        print(
            f'The positional argument "projectname" is required for deleting a virtual environment!'
        )
    else:
        print(f'Deleting venv for "{args.projectname.strip()}"')
        vlink = VenvLink()
        vlink.delete_env(args.projectname.strip())


# Executed with "python -m venvlink [params]"
if __name__ == "__main__":
    args = parser.parse_args()

    if args.init:
        init_config()
    elif args.delete:
        delete_env(args)
    else:
        create_venv(args)