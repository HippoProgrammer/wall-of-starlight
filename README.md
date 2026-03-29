# wall-of-starlight
A simple and mildly irritating Python script that walls Starlight's RMB messages to your terminal.

## Installation
### Cloning
Clone the repo to your computer and `cd` into the cloned directory.
```git clone https://github.com/HippoProgrammer/wall-of-starlight.git
cd wall-of-starlight/```

### Dependencies
Install dependencies. (Note: you may need to configure a virtual environment pre-dependency-installation, read the [tutorial](https://docs.python.org/3/tutorial/venv.html) if you get an `externally-managed-packages` error)
```pip3 install -r requirements.txt```

## Execution
Command syntax is as follows.
```python3 __main__.py <region>```
where `<region>` is the name of the NationStates region you wish to fetch RMB messages from, in HTML-safe format (e.g. Starlight -> `starlight`, The Great Storm -> `the_great_storm`).

The program will not exit unless `KeyboardInterrupt`ed.
