![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/np-8/venvlink)&nbsp;![PyPI](https://img.shields.io/pypi/v/venvlink)&nbsp;[![Downloads](https://pepy.tech/badge/venvlink)](https://pepy.tech/project/venvlink)&nbsp;![GitHub](https://img.shields.io/github/license/np-8/venvlink)

# 🔗 venvlink

The job of `venvlink` is create a *link* for the  `./venv/Scripts/activate` script inside the project folder and, if needed, create a virtual environment outside your project folder, using  `python -m venv <project_name>`.

## Table of Contents
- [Without venvlink](#without-venvlink)
- [With venvlink](#with-venvlink)
- [Motivation](#motivation)
- [Installing](#installing)
  - [Requirements](#requirements)
  - [Installation with pip](#installation-with-pip)
- [Getting started](#getting-started)
  - [Creating a virtual environment](#-creating-a-virtual-environment)
  - [Getting help](#-getting-help)
  - [Removing virtual environments](#️-removing-virtual-environments)
  - [Configuration](#️-configuration)
- [Considerations](#considerations)
    - [Special cases](#-special-cases)
    - [File structure tip](#-file-structure-tip)
- [Venvlink and other tools](#-venvlink-and-other-tools)
- [Contributing](#contributing)
## Without venvlink
This is how work with virtual environments looks like with `python -m venv venv`:

![](https://github.com/np-8/venvlink/blob/master/docs/without-venvlink.png?raw=true)

## With venvlink
With `venvlink` the virtual environment is created in a centralized folder, and only a proxy ("link") of the `activate` script is created to the project folder:
![](https://github.com/np-8/venvlink/blob/master/docs/with-venvlink.png?raw=true)

## Motivation
The reason for one using venvlink might be one or multiple from below.
### 🚫📤 don't backup venv/*
If you want to keep your virtual environments from being backed up to *e.g.* OneDrive/Dropbox or other backup service with your project files, venvlink is one way to do it. You might want to do this to save space on your cloud storage or resources on your computer / network (prevent checking and uploading new/modified files).

### 🗂️🧹centralized & tidy
If you want to centralize your virtual environments just because you think it is clean or it makes you happy.

### ✨♻️ reusability
If you want to reuse some of your virtual environments in multiple projects (sharing same imports) or want to use a general `(tmp)` virtual environment for all of your one-off testing, for example.

### 🏗️✔️relocating projects
If you want to be able to relocate projects on hard disk (on same machine) by just copy-pasting them, even with virtual environments. Or, if you want to be able rename a part of the project path without breaking the virtual environment.

### 🔑🎯 centralized, but with an `activate` script

If you want to have centralized virtual environments, but would want to activate them, without having to remember the name of the virtual environment, just by running 

```
./venv/Scripts/activate
```
The `activate` script in your project folder is just a proxy ("link") for the real `activate` script located elsewhere.



### 🗑️🤝 remove anytime
The `venvlink` philosophy is that a tool should not chain it's user. You can remove it anytime and your virtual environments and activate proxy scripts will still work. Venvlink is only used for creation of virtual environments.


### 💼✔️ works with an existing venv collection
If you happen to have already a collection of virtual environments inside one folder, you can start using them with `venvlink` right away. Just configure the `venv_folder` in the `.venvlinkrc`, and you're good to go.


### 🐍🐍 multipython
It is not a problem if you have multiple python versions installed. The syntax is

```
<path_to_python_exe> -m venvlink ...
```

Therefore, you can use `venvlink` on `Python 3.6.4 32-bit` and `Python 3.9.2 64-bit` at the same time. What you need to do is to install `venvlink` for both python versions with 

```
<path_to_python_exe> -m pip install venvlink
<path_to_another_python_exe> -m pip install venvlink
```

and the rest you can use normally. Note that virtual environments in the centralized folder will have the same python version which was used to create the virtual environment in the first place. You can later on use your main python executable to create more links for an existing virtual environment, no matter what version of python it is using. Use descriptive venv names to distinguish the venvs with different python versions, if needed.

### 🚫🔮 no magic

`venvlink` is a really simple tool. All it does is
- Runs `python -m venv projname`, inside the centralized venv folder
- Creates `activate` scripts inside your project dir, that act as proxies ("links") for the real activate scripts.

In addition there are some convenience scripts, for removing a venv or overwriting a proxy activate script. But that's about it. 

# Installing
### Requirements
`venvlink` is currently supporting only Windows, but it shouldn't be too hard to create Linux/maxOS support. I personally use only Windows, but I would be really happy to receive pull request(s) for Linux/macOS support.
## Installation with pip
```
pip install venvlink
```
<sup>For installation for development, see [CONTRIBUTING.md](docs/CONTRIBUTING.md).</sup>




# Getting started






## ✨ Creating a virtual environment

Assume that you have a project at 

```
C:\workdir\someproject\
```
and you would like to create virtual environment for that folder. 
Instead of the regular
```shell
PS C:\workdir\someproject> python -m venv venv
```

using `venvlink` one would type

```shell
PS C:\workdir\someproject> python -m venvlink project-name
```

This would create, inside your project directory, a `venv` folder with only few files (<1Kb in total), such as the `activate` script.:


```
venv
├── Scripts
│   ├── Activate.ps1
│   ├── activate
│   └── activate.bat
└── venvlink
```

and inside your `venv_folder` (located elsewhere), the actual virtual environment files (can be up to hundreds of Mb, and thousands of files):

```
project-name/
├── Include
├── Lib
│   └── site-packages
├── Scripts
│   ├── Activate.ps1
│   ├── activate
│   ├── activate.bat
│   └── deactivate.bat
├── pyvenv.cfg
└── share
```

To activate the virtual environment  `(project-name)`, you would call

```shell
PS C:\workdir\someproject> .\venv\Scripts\activate
```

which would then call transparently*

```shell
C:\Python\venvs\project-name\Scripts\activate
```
and result you having that virtual environment activated, as:

```
(project-name) PS C:\workdir\someproject> 
```

[*] assuming that you have defined the `venv_folder` to be `C:\Python\venvs\` in the `.venvlinkrc`.



## 📖❔ Getting help
You can use  the `-h` flag:
```
PS C:\somepath\project> python -m venvlink -h

usage: venvlink [-h] [--init] [-d] [-S] [projectname]

venvlink 0.3.1

positional arguments:
  projectname

optional arguments:
  -h, --help            show this help message and exit
  --init                Initiate the venvlink configuration file (.venvlinkrc)
  -d, --delete          Delete the virtual environment associated with project_name (instead of creating)
  -S, --system-site-packages
                        Give the virtual environment access to the system site-packages dir.
```

## 🗑️ Removing virtual environments
If you want to fully remove a virtual environment and all its contents, you can either run
```
python -m venvlink -d <venv_to_be_removed>
```
 or just navigate to the centralized virtual env folder, and remove the folder(s) you want. There is no centralized bookkeeping between the virtual environments and the `activate` proxies (just a one-way link from proxy to the venv), and therefore all `activate` proxies associated with the venv will stop working after deletion, or until a venv with same name is created.

If you want to just remove the link between a virtual environment and your project, you can safely remove the `activate` proxy/link from your project folder. If you are planning to create a link to another virtual environment, you can simply

```
python -m venvlink anothervenv
```

All what this does is recreates the proxy and, if anothervenv does not exist, creates anothervenv.
  


## 🛠️ Configuration

See: [Configuration](docs/configuration.md).


## Considerations

### 🔍❕ Special cases

Moving your virtual environment to centralized place means that you'll might have to tell to some tools where you have located your virtual environments. One example is  `pylint`, which needs to kown where the project venv is located, to prevent false positive `import-error`s. See: [Usage with linters (e.g. pylint)](docs/usage.md).

### 💡📁 File structure tip
Following file structure has found to be useful:
```
C:\Python\Python365\          # python installation
C:\Python\Python386\          # python installation
C:\Python\Python386-32\       # python installation
C:\Python\Python392\          # python installation
C:\Python\venvs\              # virtual environments
```
since it is easy to find `python.exe` behind for creating a venv

```
C:\Python\Python386\python.exe -m venvlink myproj
```
and it is also easy to browse the venvs when they are after a short path.

## 🍎🍌 venvlink and other tools
These tools work well together and have synergies with `venlink`:
- [venvlink and pyenv-win](docs/venvlink-and-pyenv-win.md)
- [venvlink and pew](docs/venvlink-and-pew.md)
  
Other tools and how they relate to `venvlink`: 
- [Python environment management tools](docs/python-virtual-environments.md)
## Contributing


| What?                  | How?                                                                                     |
| :--------------------- | :--------------------------------------------------------------------------------------- |
| 🐞 Found a bug?         | 🎟 <a href="https://github.com/np-8/venvlink/issues">File an Issue</a>                    |
| 🙋‍♂️ Need help?           | ❔  <a href="https://stackoverflow.com/questions/ask">Ask a question on StackOverflow</a> |
| 💡 Got a suggestion?    | <a href="https://github.com/np-8/venvlink/issues">🎫 File an Issue (feature request)</a>  |
| 🧙  Want to write code? | 🔥 <a href="./docs/CONTRIBUTING.md">Here's how you get started!</a>                       |