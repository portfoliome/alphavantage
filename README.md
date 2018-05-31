[![Build Status](https://travis-ci.org/portfoliome/alphavantage.svg?branch=master)](https://travis-ci.com/portfoliome/alpavantage)

# alphavantage

alphavantage is a Python wrapper for the Alpha Vantage API.

## Design Consideration

This library is intended to provide a simple wrapper with minimal dependencies, and does not intend to introduce pydata stack dependencies (numpy, pandas, etc.) in the future. Differences with existing wrappers for the Alpha Vantage API include:
 
### Library Differences

* No Pandas dependencies or optional dependency
* Focuses on simplifying data for ingesting
* Avoids logical branching making the code simpler (only two if statements at moment)
* Provides symbology mapping references

The library carries out some conveniences versus using the API without a wrapper.

### Conveniences

* converting timestamps to UTC time when applicable
* Simplifies record field names i.e. "4. close" -> "close"
* appends timestamp field to record vs. having timestamp act as dictionary key
* Uses time ascending list/array versus dictionary/hash for price record data structure.
* Mapping ticker symbology from other vendors
 
## Examples
```python
from alphavantage.price_history import PriceHistory, IntradayPriceHistory, filter_dividends

history = PriceHistory(output_size='compact')
results = history.get('AAPL')

history = IntradayPriceHistory(utc=True)
results = history.get('AAPL')
dividends = list(filter_dividends(results.records))

```

## Contributing
Contributions are welcome. Someone can immediately contribute by building out wrappers for the rest of the API such as FX rates or crypto prices.

## Getting Started

### Installing

```sh
pip install alphavantage
```

### Developer Installation

These instructions assume Python 3.6. It is recommended that you use conda or a virtualenv.

#### For conda install follow:
Download the [conda installer](http://conda.pydata.org/miniconda.html).
And follow setup [instructions](http://conda.pydata.org/docs/install/quick.html#id1).

#### Conda Environment

```sh
conda create --name <environment_name> python=3.6
activate <environment_name>
conda install --file requirements.txt

python setup.py install bdist_wheel
```

#### debian installation
[Instruction](https://linuxconfig.org/how-to-change-from-default-to-alternative-python-version-on-debian-linux)

Follow the instructions in the link provided. **DO NOT SUDO PIP INSTALL**. Alias the preferred Python installation by adding, for example:

```sh
alias python='/usr/bin/python3.6'
```

#### When using Pip
```sh
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt

python setup.py install bdist_wheel
```

#### Running the Tests
```sh
py.test
```
#### Running Coverage Report
```sh
py.test --cov
```
