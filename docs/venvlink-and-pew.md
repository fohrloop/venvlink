# venvlink and pew

**Note** : The following assumes that `venvlink` and `pew` are configured to use the same virtual environment folder (`WORKON_HOME` environment variable for `pew` and `venv_folder` in `.venvlinkrc` for `venvlink`)



## 🤝 Synergies
There are a lot of synergies between `pew` and `venvlink` and they can also be used together.

### listing environments

- Environments created with  `venvlink` can be listed with `pew`. For example: (create `my-linked-env` with venvlink)

```
PS C:\tmp\testproj> python -m venvlink my-linked-env
Creating venv for "my-linked-env"
12-27 19:52 venvlink     INFO     Running: "C:\Python\Python385-64\python.exe -m venv my-linked-env" with cwd="C:\Users\niko\venvs"
```

- After this, the virtual environment is visible with `pew ls`: 

```
C:\Users\niko>pew ls
another  my-linked-env  myproj  myproj2  pwr
```

### `pew show` 

The `pew show` command can be used to show python version of  environments created with `venvlink`:

```
C:\Users\niko>pew show my-linked-env
my-linked-env: Python 3.8.5
         .......
```

### `pew workon` works with virtual environments created with `venvlink`

- Below the `my-linked-env` created in the previous section with  `venvlink`  is used in another shell session with `pew`:

```
PS C:\tmp\another_testproj> pew ls
another  my-linked-env  myproj  myproj2  pwr
PS C:\tmp\another_testproj> pew workon my-linked-env
Launching subshell in virtual environment. Type 'exit' to return.
PowerShell 6.2.3
Copyright (c) Microsoft Corporation. All rights reserved.

https://aka.ms/pscore6-docs
Type 'help' to get help.

PS C:\tmp\another_testproj> python
Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys; sys.executable
'C:\\Users\\niko\\venvs\\my-linked-env\\Scripts\\python.exe'
``` 

## Using `venvlink` to create link to `pew` virtual environments
It is possible to create `activate` scripts to project folder(s) with `venlink` that use virtual environments created with `pew`. For example:

- Creating new virtual environment `new-env` with `pew`:

```
C:\Users\niko>pew new some-env
created virtual environment CPython3.8.5.final.0-64 in 773ms
  creator CPython3Windows(dest=C:\Users\niko\venvs\some-env, clear=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=C:\Users\niko\AppData\Local\pypa\virtualenv)
    added seed packages: pip==20.2.4, setuptools==50.3.2, wheel==0.35.1
  activators BashActivator,BatchActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator
Launching subshell in virtual environment. Type 'exit' to return.
Microsoft Windows [Version 10.0.19041.685]
(c) 2020 Microsoft Corporation. All rights reserved.
```

- Using that virtual environment in a project, and creating a link to it using `venvlink`: 
```
PS C:\tmp\another-testproj> python -m venvlink some-env
Creating venv for "some-env"
The virtual environment for a projectname "some-env" exists already. If you use the name "some-env", you will SHARE the virtual environment with the other project(s) using the same name.
Continue?

[Y] Yes [N] No, give new name. [A] Abort: Y
PS C:\tmp\another-testproj> .\venv\Scripts\activate
venvlink: Activating virtual env in "C:\Users\niko\venvs\some-env"
(some-env) PS C:\tmp\another-testproj> python
Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys; sys.executable
'C:\\Users\\niko\\venvs\\some-env\\Scripts\\python.exe'
```

## 🍎🍌 Differences
- When using `pew workon` to activate a virtual environment, the name of the virtual environment does not show in the shell prompt. It can be checked with `pew show` command.
-  When using `activate` script created with `venvlink` (or python `venv`), the name of the active virtual environment is shown in parenthesis at the left side of the shell prompt.
- When using `pew workon`, the virtual environment can be activated from anywhere using the ***name*** of the virtual environment. When using `venvlink`, the virtual environment can be activated using the ***`activate` script*** which is located the project folder (can also be called anywhere). 
- When creating virtual environments, one must be in a project folder, to create a virtual environment with `venvlink`, but you can create virtual environment anywhere using `pew`. 
- The activate script using `venvlink` will colorize the virtual environment name, if using Powershell.