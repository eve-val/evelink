EVELink - Python Bindings for the EVE API
=========================================

EVELink provides a means to access the [EVE XML API](https://eveonline-third-party-documentation.readthedocs.io/en/latest/xmlapi/) from Python.

[![PyPI](http://img.shields.io/pypi/v/EVELink.svg)](https://pypi.python.org/pypi/EVELink)


Example Usage
-------------

```python
import evelink.api  # Raw API access
import evelink.char # Wrapped API access for the /char/ API path
import evelink.eve  # Wrapped API access for the /eve/ API path

# Using the raw access level to get the name of a character
api = evelink.api.API()
response = api.get('eve/CharacterName', {'IDs': [1]})
print response.result.find('rowset').findall('row')[0].attrib['name']

# Using the wrapped access level to get the name of a character
eve = evelink.eve.EVE()
response = eve.character_name_from_id(1)
print response.result

# Using authenticated calls
api = evelink.api.API(api_key=(12345, 'longvcodestring'))
id_response = eve.character_id_from_name("Character Name")
char = evelink.char.Char(char_id=id_response.result, api=api)
balance_response = char.wallet_balance()
print balance_response.result
```


Dependencies
------------
EVELink uses the `six` library to maintain compatibility with both Python 2 and 3.
This is the only required dependency.

However, EVELink will also make use of the `requests` library if it is available in your Python environment,
as it enables the use of a single persistent HTTP connection for a sequence of EVE API calls for a
given API instance. This eliminates the overhead of establishing a new TCP/IP connection for every
EVE API call, which in turn results in an overall performance increase. For this reason it is highly
recommended to have `requests` installed, but to keep up with the spirit of keeping EVELink free from
external dependencies, it is left to be an option for all users.

If you are developing on EVELink itself (to contribute to this project), the following packages are
required in order to run the tests:

 - `mock`
 - `nose`
 - `unittest2` (Python 2.x only)

A `requirements_{py2,py3}.txt` is provided as part of the repository for developer convenience.


Design
------

EVELink aims to support 3 "levels" of access to EVE API resources: raw, wrapped, and object.

### Raw access

Raw is the lowest level of access - it's basically just a small class that takes an API path and parameters and the result portion of the `APIResult` is an `xml.etree.ElementTree` object. You probably don't want to use this layer of access, but it can be useful for API calls that EVELink doesn't yet support at a higher level of access.

All `APIResult` objects also contain timestamp and expires fields, which indicate the time when the result was obtained from the API and the time when the cached value expires, respectively.

### Wrapped access

Wrapped is the middle layer of access. The methods in the wrapped access layer still map directly to EVE API endpoints, but are "nicer" to work with. They're actual Python functions, so you can be sure you're passing the right arguments. Their `APIResult` result fields contain basic Python types which are simple to work with.

### Object access

*(not yet implemented)*

Object access is the highest layer of access and the most encapsulated. Though implementation is being deferred until after the wrapped access layer is more complete, the goal here is to essentially emulate a set of ORM objects, allowing you do to things like `Character(id=1234).corporation.name` to fetch the name of the corporation that the character with ID `1234` is in.


Development
-----------

[![Build Status](https://travis-ci.org/eve-val/evelink.png?branch=master)](https://travis-ci.org/eve-val/evelink) [![Coverage Status](https://img.shields.io/coveralls/eve-val/evelink.svg)](https://coveralls.io/r/eve-val/evelink?branch=master)

To acquire a development copy of the library and set up the requirements for testing:

```bash
$ git clone https://github.com/eve-val/evelink.git
$ cd evelink
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements_{py2,py3}.txt
```

To run the tests:

```bash
$ nosetests
```

To run the tests, including the appengine ones (this requires that you have Google AppEngine's python SDK installed):

```bash
$ nosetests --with-gae
```

Additional information for developers is available [here](https://github.com/eve-val/evelink/wiki/Development-Guidelines).
