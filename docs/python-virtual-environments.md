# Python virtual environments
Here is a list of different tools and how they relate to `venvlink`.

## [pew](https://github.com/berdario/pew) (Python Environment Wrapper)
- Written in pure python and leverages [inve](https://datagrok.org/python/activate/) ("inside this virtual environment, (run this command)…")
- Can be installed with `pip`
- Keeps all virtual environments in single location, which by default is either defined by environment variable `XDG_DATA_HOME` or `WORKON_HOME`.
- Was originally a rewrite of virtualenvwrapper

## [pipenv](https://github.com/pypa/pipenv)
- 21.4k stars on GitHub (2020-12-21)
- Virtual environments are created in single folder
- Tool that is intended to replace both, `pip` and `venv`/`virtualenv`.
- Python versions: automatically installs required python versions, if `pyenv` is available.
- Keeps track of what python packages you install or remove, using a `Pipfile`.


## pyenv


## pyvenv
This was a short-lived tool (introduced in Python 3.3, [deprecated in 3.6](https://docs.python.org/dev/whatsnew/3.6.html#deprecated-features)) for creating virtual environments and was superceded by `python -m venv`. 

## venv
The [venv](https://docs.python.org/3/library/venv.html) is a module which is included in the CPython standard library since Python 3.3. It is commonly used with command

```
python -m venv venv
```

and this is the command `venvlink` uses internally to create virtual environments. 

### Pros
- Comes with standard library (Python 3.3+)
- Easy to use. Lightweight.
  
## virtualenv

## [virtualenvwrapper](https://github.com/bernardobarreto/virtualenvwrapper)
- It is a set of extensions over top of `virtualenv`.
- Versions
  - Fork: [bernardobarreto/virtualenvwrapper](https://github.com/bernardobarreto/virtualenvwrapper) (33 stars)
- Commands

```
lsvirtualenv
mkvirtualenv [mkvirtualenv-options] [virtualenv-options] <name>
    [mkvirtualenv-options]
    -h  Print help text.
workon [<name>]
deactivate
rmvirtualenv <name>
```
## [virtualenvwrapper-win](https://github.com/davidmarble/virtualenvwrapper-win)

- Created virtual environments into: `WORKON_HOME`, or if not defined, to `%USERPROFILE%\Envs`.


--- 

# Python version switchers

### [pywin](https://github.com/davidmarble/pywin)
- Works with: virtualenvwrapper-win