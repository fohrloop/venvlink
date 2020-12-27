## 🛠️ Configuration


### Initializing configure file

To create the initial `.venvlinkrc` file, or reinitialize it, use command

```
python -m venvlink --init
```

The initialization command is ran automatically, if `.venvlinkrc` does not exists, and user tries to create a virtual environment.
### Location of `.venvlinkrc`
The configuration file, `.venvlinkrc` should be located at 
```
%USERPROFILE%\.venvlinkrc
```
which usually translates into  `C:\Users\USER\.venvlinkrc`. 

### Contents of `.venvlinkrc`
Here is an example default config (copy-paste):

```
[general]
venv_folder = C:\Users\USER\venvs
```
**[general]: venv_folder** <br>
This is the folder where all the virtual environment are stored, in subfolders. 