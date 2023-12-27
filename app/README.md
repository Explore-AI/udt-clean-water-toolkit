NB: This package is a module that can be run independently as well as within another project. Therefore, use relative imports only

# app

## 1. Requirements

- tbc
- cleanwater (from this package)

These packages can be installed with the instructions in Section 2.

## 2. Development

Create a python3 virtual environment and install required modules. For example using pip:

```
# from project root dir

python3 -m venv app/venv

source app/venv/bin/activate

pip install -r app/requirements.txt -r app/dev-requirements.txt 
```

Before running the `app` for development one needs to package and install the `cwm` module in dev mode:

```
# assuming you area already in the `app` virtual environment

cd cwm/

pip install -e .

# The module can now be imported with

import cleanwater
```




