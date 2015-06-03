from evelink import api

def parse_planetary_colonies(api_results):
    result = {}
    rowset = api_results.find('rowset')
    for row in rowset.findall('row'):
        # shortcut to make the following block less painful
        a = row.attrib
        planetID = int(a['planetID'])
        result[planetID] = {
            'id': planetID,
            'system': {
                'id': int(a['solarSystemID']),
                'name': a['solarSystemName'],
            },
            'planet': {
                'name': a['planetName'],
                'type': int(a['planetTypeID']),
                'type_name': a['planetTypeName'],
            },
            'owner': {
                'id': int(a['ownerID']),
                'name': a['ownerName'],
            },
            'last_update': api.parse_ts(a['lastUpdate']),
            'upgrade_level': int(a['upgradeLevel']),
            'number_of_pins': int(a['numberOfPins']),
        }

    return result


def parse_planetary_links(api_results):
    result = {}
    rowset = api_results.find('rowset')
    for row in rowset.findall('row'):
        # shortcut to make the following block less painful
        a = row.attrib
        sourceID = int(a['sourcePinID'])
        result[sourceID] = {
            'source_id': sourceID,
            'destination_id': int(a['destinationPinID']),
            'link_level': int(a['linkLevel']),
        }

    return result

def parse_planetary_pins(api_results):
    result = {}
    rowset = api_results.find('rowset')
    for row in rowset.findall('row'):
        # shortcut to make the following block less painful
        a = row.attrib
        pinID = int(a['pinID'])
        if pinID not in result:
            result[pinID] = {
                'id': pinID,
                'type': {
                    'id': int(a['typeID']),
                    'name': a['typeName'],
                },
                'schematic': int(a['schematicID']),
                'last_launch_ts': api.parse_ts(a['lastLaunchTime']),
                'cycle_time': int(a['cycleTime']),
                'quantity_per_cycle': int(a['quantityPerCycle']),
                'install_ts': api.parse_ts(a['installTime']),
                'expiry_ts': api.parse_ts(a['expiryTime']),
                'content': {
                    'type': int(a['contentTypeID']),
                    'name': a['contentTypeName'],
                    'quantity': int(a['contentQuantity']),
                    'deprecated': 'Use the "contents" field instead',
                },
                'contents': {},
                'loc': {
                    'long': float(a['longitude']),
                    'lat': float(a['latitude']),
                },
            }

        if a['contentTypeID'] != '0':
            contentID = int(a['contentTypeID'])
            result[pinID]['contents'][contentID] = {
                'type': contentID,
                'name': a['contentTypeName'],
                'quantity': int(a['contentQuantity']),
            }


    return result

def parse_planetary_routes(api_results):
    result = {}
    rowset = api_results.find('rowset')
    for row in rowset.findall('row'):
        # shortcut to make the following block less painful
        a = row.attrib
        routeID = int(a['routeID'])
        result[routeID] = {
            'id': routeID,
            'source_id': int(a['sourcePinID']),
            'destination_id': int(a['destinationPinID']),
            'content': {
                'type': int(a['contentTypeID']),
                'name': a['contentTypeName'],
            },
            'quantity': int(a['quantity']),
            'path': tuple(int(a['waypoint%d' % n]) for n in range(1,6)),
        }

    return result
