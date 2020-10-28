![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/np-8/venvlink)&nbsp;![PyPI](https://img.shields.io/pypi/v/venvlink)&nbsp;![PyPI - Downloads](https://img.shields.io/pypi/dm/venvlink)&nbsp;![GitHub](https://img.shields.io/github/license/np-8/venvlink)


# 🔗 venvlink

Create virtual environments in one centralized folder, and have `venv/Scripts/activate` still in your working folder (as hard links)!

# Installing
```
pip install venvlink
```

# Usage

## Simple example

Assume that you have a project at 

```
C:\workdir\someproject\
```
and that you are in command line inside that folder (call it, `<project_root>`). Then, you would like to create virtual environment for that folder.

Instead of the regular
```python
# at C:\workdir\someproject\
python -m venv venv
```

One would type

```python
# at C:\workdir\someproject\
python -m venvlink project-name
```

This would create the following folders:

```
C:\workdir\someproject\venv
   ^-- This has only few hardlinked files, such as the "activate" script.

C:\<venvlink-venv-path>\project-name
   ^--- The actual virtual environment files are here!
```

The first folder is for using the virtual environment normally, just like you have used to (running `venv/Scripts/activate`) and the second folder is for storing the actual virtual environment files.

