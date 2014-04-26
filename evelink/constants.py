ACCOUNT = 'account'
CHARACTER = 'char'
CORPORATION = 'corp'

BLUEPRINT_ORIGINAL = -1
BLUEPRINT_COPY = -2

_role_type_bases = {
    'global': '',
    'at_hq': 'AtHQ',
    'at_base': 'AtBase',
    'at_other': 'AtOther',
}

class Char(object):
    corp_roles = dict((k, 'corporationRoles' + v) for k,v in _role_type_bases.items())

class Corp(object):
    role_types = dict((k, 'roles' + v) for k,v in _role_type_bases.items())
    grantable_types = dict((k, 'grantableRoles' + v) for k,v in _role_type_bases.items())

    pos_states = ('unanchored', 'anchored', 'onlining', 'reinforced', 'online')

    pos_permission_entities = (
            'Starbase Config',
            'Starbase Fuel Tech',
            'Corporation Members',
            'Alliance Members',
        )

class Industry(object):
    job_status = ('failed', 'delivered', 'aborted', 'gm-aborted', 'inflight-unanchored', 'destroyed')

class Market(object):
    order_status = ('active', 'closed', 'expired', 'cancelled', 'pending', 'deleted')

class APIKey(object):
    key_types = {
        # This maps from EVE API values (keys) to our local constants (values)
        'Account': ACCOUNT,
        'Character': CHARACTER,
        'Corporation': CORPORATION,
    }
