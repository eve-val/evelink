EVELink - Python Bindings for the EVE API
=========================================

EVELink provides a means to access the [EVE API](http://wiki.eveonline.com/en/wiki/EVE_API_Functions) from Python.


Example Usage
-------------

```python
import evelink.api # Raw API access
import evelink.eve # Wrapped API access for the /eve/ API path

# Using the raw access level to get the name of a character
api = evelink.api.API()
result = api.get('eve/CharacterName', {'IDs': [1]})
print result.find('rowset').findall('row')[0].attrib['name']

# Using the wrapped access level to get the name of a character
eve = evelink.eve.EVE()
print eve.character_name_from_id(1)

# Using authenticated calls
api = evelink.api.API(api_key=(12345, 'longvcodestring'))
charid = eve.character_id_from_name("Character Name")
char = evelink.char.Char(char_id = charid, api=api)
print char.wallet_balance()
```


Dependencies
------------
**EVELink does not require any extra dependencies for normal operation.**

If you are developing on EVELink, however, the following packages are required in order to run the tests:

 - `mock`
 - `nose`
 - `unittest2`

A `requirements.txt` is provided as part of the repository for developer convenience.


Design
------

EVELink aims to support 3 "levels" of access to EVE API resources: raw, wrapped, and object.

### Raw access

Raw is the lowest level of access - it's basically just a small class that takes an API path and parameters and returns an `xml.etree.ElementTree` object. You probably don't want to use this layer of access, but it can be useful for API calls that EVELink doesn't yet support at a higher level of access.

### Wrapped access

Wrapped is the middle layer of access. The methods in the wrapped access layer still map directly to EVE API endpoints, but are "nicer" to work with. They're actual Python functions, so you can be sure you're passing the right arguments. They return basic Python types which makes the results simple to use.

### Object access

*(not yet implemented)*

Object access is the highest layer of access and the most encapsulated. Though implementation is being deferred until after the wrapped access layer is more complete, the goal here is to essentially emulate a set of ORM objects, allowing you do to things like `Character(id=1234).corporation.name` to fetch the name of the corporation that the character with ID `1234` is in.


Development
-----------

To acquire a development copy of the library and set up the requirements for testing:

```bash
$ git clone https://github.com/eve-val/evelink.git
$ cd evelink
$ virtualenv venv --distribute
$ source venv/bin/activate
$ pip install -r requirements.txt
```

To run the tests:

```bash
$ nosetests
```

To run the tests, including the appengine ones (this requires that you have Google AppEngine's python SDK installed):

```bash
$ cd tests
$ nosetests --with-gae
```

Additional information for developers is available [here](https://github.com/eve-val/evelink/wiki/Development-Guidelines).
