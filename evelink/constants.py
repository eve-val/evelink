CHARACTER = 'char'
CORPORATION = 'corp'

class Char(object):
    corp_roles = {'roles': 'corporationRoles',
                  'at_hq': 'corporationRolesAtHQ',
                  'at_base': 'corporationRolesAtBase',
                  'at_other': 'corporationRolesAtOther'}

class Industry(object):
    job_status = ('failed', 'delivered', 'gm-aborted', 'inflight-unanchored', 'destroyed')

class Market(object):
    order_status = ('active', 'closed', 'expired', 'cancelled', 'pending', 'deleted')

class APIKey(object):
    key_types = {
        # This maps from EVE API values (keys) to our local constants (values)
        'Character': CHARACTER,
        'Corporation': CORPORATION,
    }
