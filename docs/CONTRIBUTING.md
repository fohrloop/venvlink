# Contributing

This is the workflow on how one would contribute on this project.

1) Fork this project on GitHub
2) Clone the fork of venv from GitHub to your own PC
3) Create a virtual environment and activate it. Install venvlink to the virtual environment in *editable state* with 

```
pip install -e .
```
where `.` denotes the current directory. If you're not in the project root directory navigate into it, or replace `.` with full filepath pointing to the folder with the `setup.py`. (remember to quote the path if it contains spaces)

also install `pytest` with `pip`.

4) Make some changes
5) Write test for the changes, if applicable, to the `tests` folder. The naming convention is `test_<higher-level-topic>.py`. Inside the test modules, write functions with name `test_name_of_the_test`. This way they are discovered automatically by `pytest`.
6) Run tests with

```
python -m pytest .\tests
```

7) When tests look ok, and you are happy with the code, stage the changes, and commit them, one piece at a time. Try to have *atomic* (small) commits, and not one large commit with *lots* of stuff inside it.
8) Git push to your fork in GitHub
9) Create pull request on GitHub. Usually there is some discussion about the changes and perhaps some iterations before the changes are merged.

As a general tip (applies to any open source project), if you have very wild ideas, it is better to discuss with the maintainer(s) about it before implementing it, for example in a GitHub Issue. This way the contribution is most effective.  