# venvlink and pipenv
`venvlink` is very different tool than `pipenv`. (See also: [python-virtual-environments](python-virtual-environments.md)).

## Scopes
- `venvlink` is a virtual environment management tool, where the main purpose is just to create links to `activate` scripts of virtual environments inside project folders. 
- `pipenv` is a dependency manager tool which replaces `pip`, and creates virtual environment automatically, mapping projects to their virtual environments. It is highly optimized for a 1:1 workflow (1 venv per project). 

## Creating virtual environments

- `pipenv` creates virtual environments automatically when running `pipenv install` in the project folder. The virtual environment name will be project's root directory plus a hash from the full path of the project's root, e.g. `myproject-a83de32`.
- Creating virtual environments with `venvlink` is the same as creating virtual environments with `python -m venv <project_name>`. It is also possible to just create a link to existing virtual environment with `venvlink`.  

## Number of virtual environments
- Because `pipenv` follows 1:1 mapping between projects and virtual environments, you will always have as many virtual environments as projects started with `pipenv`. There is no way to reuse virtual environments.
- With `venvlink`, it is possible to create as many links as you wish to same virtual environment; you can have only 6 virtual environments that serve 20 projects. 

## Activating / using virtual environments
- With `pipenv` it is possible to run python scripts without activating virtual environment with `pipenv run ...`, when command is ran in the project folder.
- Another way activating  venvs in `pipenv` is running `pipenv shell` inside project folder or one of it's subfolders.
- Using virtual environments *outside* the project folder would looks something like this in `pipenv`: Let's say you have two dependent `.py` files in same folder and you want to run them in a virtual environment of `myproj`, the process would be
  - `cd` into the project folder (`myproj`)
  - `pipenv shell` to activate the virtual environment
  - `cd` into the folder with the two `.py` files.
  - Run the script(s)
- With `venvlink`, one would activate the virtual environment using the `activate` script ("link") located in the project folder. The cwd can be anything when the `activate` script is ran.
- With `venvlink` it is also possible to run the python executable directly with `<venv_folder>/<venv_name>/Scipts/python.exe ...`, if needed (as with when using `venv` without `venvlink`)
-  It is also possible to use [`pew` with venvlink](venvlink-and-pew.md). (and activate virtual environments using `pew workon myproject`)
  - `venvlink` (0.5.0+) has support for automatically activating and deactivating virtual environments in Powershell using [venvlink-autoenv](https://github.com/np-8/venvlink-autoenv-powershell).

## Changing virtual environments

- With `pipenv`, there exists 1:1 mapping between virtual environments and projects; The project also can only use it's own virtual environment.  Changing virtual environment is possible only by removing and recreating the virtual environment altogether.
- With `venvlink` it is possible to point a project to new virtual environment just by `python -m venvlink new_venv_name`. It is possible to change a virtual environment really fast, and it can include changing the python version. 
- `venvlink` can also create links pointing to centralized virtual environments created with any other tool, such as [`pew`](venvlink-and-pew.md). 

## Relocating projects
Sometimes projects need to be relocated or the project path needs to be renamed slightly. 


- If project folder is renamed or relocated*, `pipenv` cannot find the virtual environment anymore. (see [this](https://pipenv.pypa.io/en/latest/install/#virtualenv-mapping-caveat) and [this](https://github.com/pypa/pipenv/issues/796#issuecomment-333376625))
- If project folder is renamed or relocated withing the same computer, the `activate` scripts created with `venvlink` will continue working, since they are just one-way links to the real activate scripts. 
    
<sup>\* When using the the centralized folder for virtual environments with pipenv.</sup>
  