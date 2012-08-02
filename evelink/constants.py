CHARACTER = 'char'
CORPORATION = 'corp'

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
