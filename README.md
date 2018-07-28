# Cayuse Interview Homework
### Michael Lane

## Setup

First ensure that you have python >= 3.6 installed on your system. 
To verify, from your comand prompt run this:

```bash
python3 -V
``` 

Once you have python >= 3.6, then set up the script by running this:

```bash
python3 setup.py install
```

You must have your OpenWeather and Google Maps API keys installed
in the environment in order to run this. So run this:

```bash
export GOOGLE_MAPS_API_KEY=<YOUR KEY HERE>
export OPEN_WX_API_KEY=<YOUR KEY HERE>
```

If you'd like to see debugging output, you can do this:

```bash
export LOGGING_LEVEL=DEBUG
```

## Run

This script comes with a CLI entrypoint called `city-info`. So you
can run it like this:

```bash
city-info --zip 97201
```

This should return the information about Portland, OR.


## Development

The development environment uses `pipenv`. Once you have pipenv
installed, run this:

```bash
pipenv --three
pipenv install
```

Create a `.env` file following the guidelines in the `.env.template`
file. Then do this:

```bash
pipenv shell
python setup.py install
city-info --zip 97214
```
