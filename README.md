# quinbot

# Install Dependencies

To install/use quinbot, make sure you have python 3 installed and available. If you have
[pyenv](https://github.com/pyenv/pyenv), this project will automatically work. If not,
ensure you have python 3 by running:

```
python --version
```

First, create a virtualenv to install all packages:

```
virtualenv .env
```

Then activate that virtualenv (this should work with WSL on Windows as well):

```
. .env/bin/activate
```

## Install Dependencies (mac)

To install the requirements on Mac, you will first need `portaudio` installed, which you
can do using [homebrew](https://brew.sh/) or another package manager of your choice:

```
brew install portaudio
```

Then install all of the dependencies of the project:

```
pip install -r requirements-mac.txt
```

# Install Dependencies (windows)

To install the requirements on Windows, you will first need `portaudio` installed, which
you can do using the following commands:

```
pip install pipwin
pipwin install pyaudio
```

Then install all of the dependencies of the project:

```
pip install -r requirements-windows.txt
```

# Running the Project

After installing the dependencies, you should be able to then run the project with
`./chat.py` or `python chat.py`.
