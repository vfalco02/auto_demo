# auto_demo

This is a test Python automation project using [Selene](https://github.com/yashaka/selene) and [PyTest](https://github.com/pytest-dev/pytest).

This project automates the [SauceLabs](https://saucelabs.com/) automation demo site https://www.saucedemo.com

## Purpose

The purpose of this project is to show how to use the [Page-Object-Model](https://www.guru99.com/page-object-model-pom-page-factory-in-selenium-ultimate-guide.html) with PyTest to automate a website.

The intent is that this grows to cover more advanced concepts.

## Setup

This project uses python 3.8. Follow the below steps to setup the project:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pytest
```

## Contributing

Add pre-commit and install it. Pre-commit will be used to run [Flake8](https://flake8.pycqa.org/en/latest/) and [yapf](https://github.com/google/yapf) against the repository upon commit.

```
pre-commit install
```