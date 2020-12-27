# venvlink and pyenv-win

Venvlink works very well together with [pyenv-win](https://github.com/pyenv-win/pyenv-win). The `pyenv-win` will take care of switching the `python` version and `venvlink` will take care of creating the virtual environments.

## what is pyenv?

[pyenv](https://github.com/pyenv/pyenv) is a Unix (Linux & macOS) tool used to manage your python version. That is, 
- It can install python versions
- It can be used to switch between python versions, rather than you modifying the operating system `PATH` environmental variable. I.e. it can be used to change your *global* Python version.

It does not support Windows, but it has a Windows version:  pyenv-win. 


## Notes about python versions and `venvlink`
- Note1: The `venvlink` must be installed separately for each python version (`pip install venvlink`)
- Note2: The virtual environments created with `venvlink` will retain the python version even if you would change the local/global python version with `pyenv-win` afterwards; only the version used to *create* the virtual environment matters
- Note3: If one would create first virtual environment `myproj` with Python 3.8.6 and then create (another) link to it with `venlink`, using *any* python version, the version of python in `myproj` would still be 3.8.6 (if the virtual environment is not completely removed/recreated)

## `venvlink` + `pyenv-win` examples
### Example using `pyenv global`

First, changing global python to version `3.8.7` with `pyenv-win`:
```
PS C:\tmp\project_1> pyenv global 3.8.7
PS C:\tmp\project_1> pyenv version
3.8.7 (set by C:\Users\niko\.pyenv\pyenv-win\version)
```
then, creating virtual environment `proj1` with `venvlink` to the folder `project_1`:
```
PS C:\tmp\project_1> python -m venvlink proj1
Creating venv for "proj1"
12-27 23:32 venvlink     INFO     Running: "C:\Users\niko\.pyenv\pyenv-win\versions\3.8.7\python.exe -m venv proj1" with cwd="C:\Users\niko\venvs"
```
one can see already from the output that the `pyenv-win` installed python version `3.8.7` was used to create the virtual environment. Then, changing to `project_2` folder, and changing the global python to version `3.9.1`: 
```
PS C:\tmp\project_1> cd ..\project_2\
PS C:\tmp\project_2> pyenv global 3.9.1
PS C:\tmp\project_2> pyenv version
3.9.1 (set by C:\Users\niko\.pyenv\pyenv-win\version)
```
Then, creating virtual environment `proj2` with `venvlink` to `project_2`:
```
PS C:\tmp\project_2> python -m venvlink proj2
Creating venv for "proj2"
12-27 23:33 venvlink     INFO     Running: "C:\Users\niko\.pyenv\pyenv-win\versions\3.9.1\python.exe -m venv proj2" with cwd="C:\Users\niko\venvs"
```
One can see already from the output that the `pyenv-win` installed python version `3.9.1` was used to create the virtual environment. Now, checking the python versions with `python` shells:
```
PS C:\tmp\project_2> cd..
PS C:\tmp> .\project_1\venv\Scripts\activate
venvlink: Activating virtual env in "C:\Users\niko\venvs\proj1"
(proj1) PS C:\tmp> python
Python 3.8.7 (tags/v3.8.7:6503f05, Dec 21 2020, 17:59:51) [MSC v.1928 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> quit()
(proj1) PS C:\tmp> deactivate
PS C:\tmp> .\project_2\venv\Scripts\activate
venvlink: Activating virtual env in "C:\Users\niko\venvs\proj2"
(proj2) PS C:\tmp> python
Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 17:08:21) [MSC v.1927 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> quit()
(proj2) PS C:\tmp> deactivate
```

### Example using `pyenv local`

`pyenv-win` also supports using python versions given locally for the project folder. In this case, the project folder will have `.python-version` file containing the name of the python version.

Below is a full example of how using the `pyenv local` command with `venvlink` would look like:

```
PS C:\tmp\project_1> pyenv version
3.9.1 (set by C:\Users\niko\.pyenv\pyenv-win\version)
PS C:\tmp\project_1> pyenv local 3.8.7
PS C:\tmp\project_1> ls


    Directory: C:\tmp\project_1

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        27/12/2020    23:36              7 .python-version

PS C:\tmp\project_1>  cat .\.python-version
3.8.7
PS C:\tmp\project_1> cd ..
PS C:\tmp> cd .\project_2\
PS C:\tmp\project_2> ls
PS C:\tmp\project_2> pyenv version
3.9.1 (set by C:\Users\niko\.pyenv\pyenv-win\version)
PS C:\tmp\project_2> pyenv local 3.9.1
PS C:\tmp\project_2> cd ..
PS C:\tmp> cd .\project_1\
PS C:\tmp\project_1> python
Python 3.8.7 (tags/v3.8.7:6503f05, Dec 21 2020, 17:59:51) [MSC v.1928 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> quit()
PS C:\tmp\project_1> python -m venvlink proj1
Creating venv for "proj1"
12-27 23:38 venvlink     INFO     Running: "C:\Users\niko\.pyenv\pyenv-win\versions\3.8.7\python.exe -m venv proj1" with cwd="C:\Users\niko\venvs"
PS C:\tmp\project_1> cd ..\project_2\
PS C:\tmp\project_2> python -m venvlink proj2
Creating venv for "proj2"
12-27 23:38 venvlink     INFO     Running: "C:\Users\niko\.pyenv\pyenv-win\versions\3.9.1\python.exe -m venv proj2" with cwd="C:\Users\niko\venvs"
```
As it can be seen from the output of the `venvlink` commands, the correct local python versions of `pyenv-win` were used to create the virtual environments.