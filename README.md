Pipenv To DEB
=============

[![Build Status](https://travis-ci.org/matthewfranglen/pipenv2deb.svg?branch=master)](https://travis-ci.org/matthewfranglen/pipenv2deb)

This tool can convert a pipenv python project into a debian package.
The debian package will install the source code and virtual environment into the `/usr/local/src` folder.
Any python scripts in the project can be invoked through auto generated shims.

Synopsis
--------

```
pipenv2deb Pipfile setup.py
```

This produces a debian package that contains the source code and shims for every script registered in `setup.py`.
It will use the project name from `setup.py`.
This is the preferred way to use this tool.

```
pipenv2deb Pipfile
```

This produces a debian package that contains only the source code.
It will use the name of the folder containing the Pipfile as the project name.

```
pipenv2deb Pipfile --script foo.py --script bar.py --name foo-bar
```

This produces a debian package that contains the source code and shims for the `foo.py` and `bar.py` scripts.
It will use the `foo-bar` name as the project name.

Details
-------

This uses pipenv and pyenv to isolate the environment.
The environment will be created inside the project folder in `/usr/local/src`.
The only files created outside this folder are the shims.
