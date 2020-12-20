
## Usage with linters (e.g. pylint)

Linters like `pylint` try to search for the packages intelligently from a virtual environment, if such exists. Placing virtual environment files outside of `<project>\venv\`, to for example `C:\Python\venvs\myproj` will have the side effect that linters might not find your modules. This might cause false positive `import-error`s, like the one below.

![](docs/pylint-error.png)

### Fixing false positive `import-error`s
You have to tell to the linter that you are using, where to look for the modules. 

**`pylint`**<br><br>
Add following init hook

```
--init-hook "import sys; sys.path.insert(0, 'C:/Python/venvs/myenv/Lib/site-packages')"
```
- Replace `'C:/Python/venvs/myenv'` with the virtual environment path of your project
- Note that the path separator is ***forward*** slash `/`


**VSCode & `pylint`**<br><br>
To configure `pylint` in VSCode, you need to
- Open `Preferences: Open Workspace Settings (JSON)` (Ctrl+Shift+P)
- Add there the following:

```json
{
    "python.linting.pylintArgs": [
        "--init-hook",
        "import sys; sys.path.insert(0, 'C:/Python/venvs/myenv/Lib/site-packages')",
        "--disable=all",
        "--enable=F,E,unreachable,duplicate-key,unnecessary-semicolon,global-variable-not-assigned,unused-variable,binary-op-exception,bad-format-string,anomalous-backslash-in-string,bad-open-mode"
    ],
}
```
- The `--disable=all` and `--enable=...` are optional, but you want to keep them if you are not using a `pylintrc` file, and you are used to the [default filtering VSCode does for you](https://code.visualstudio.com/docs/python/linting#_default-pylint-rules). 