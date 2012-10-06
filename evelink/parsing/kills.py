from evelink import api

def parse_kills(api_result):
    rowset = api_result.find('rowset')
    result = {}
    for row in rowset.findall('row'):
        a = row.attrib
        kill_id = int(a['killID'])
        result[kill_id] = {
            'id': kill_id,
            'system_id': int(a['solarSystemID']),
            'time': api.parse_ts(a['killTime']),
            'moon_id': int(a['moonID']),
        }

        victim = row.find('victim')
        a = victim.attrib
        result[kill_id]['victim'] = {
            'id': int(a['characterID']),
            'name': a['characterName'],
            'corp': {
                'id': int(a['corporationID']),
                'name': a['corporationName'],
            },
            'alliance': {
                'id': int(a['allianceID']),
                'name': a['allianceName'],
            },
            'faction': {
                'id': int(a['factionID']),
                'name': a['factionName'],
            },
            'damage': int(a['damageTaken']),
            'ship_type_id': int(a['shipTypeID']),
        }

        result[kill_id]['attackers'] = {}

        rowsets = {}
        for rowset in row.findall('rowset'):
            key = rowset.attrib['name']
            rowsets[key] = rowset

        for attacker in rowsets['attackers'].findall('row'):
            a = attacker.attrib
            attacker_id = int(a['characterID'])
            result[kill_id]['attackers'][attacker_id] = {
                'id': attacker_id,
                'name': a['characterName'],
                'corp': {
                    'id': int(a['corporationID']),
                    'name': a['corporationName'],
                },
                'alliance': {
                    'id': int(a['allianceID']),
                    'name': a['allianceName'],
                },
                'faction': {
                    'id': int(a['factionID']),
                    'name': a['factionName'],
                },
                'sec_status': float(a['securityStatus']),
                'damage': int(a['damageDone']),
                'final_blow': a['finalBlow'] == '1',
                'weapon_type_id': int(a['weaponTypeID']),
                'ship_type_id': int(a['shipTypeID']),
            }

        def _get_items(rowset):
            items = []
            for item in rowset.findall('row'):
                a = item.attrib
                type_id = int(a['typeID'])
                items.append({
                    'id': type_id,
                    'flag': int(a['flag']),
                    'dropped': int(a['qtyDropped']),
                    'destroyed': int(a['qtyDestroyed']),
                })

                containers = item.findall('rowset')
                for container in containers:
                    items.extend(_get_items(container))

            return items

        result[kill_id]['items'] = _get_items(rowsets['items'])

    return result
