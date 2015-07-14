from evelink import api

def parse_bookmarks(api_results):
    result = {}
    folders = api_results.find('rowset')
    for row in folders.findall('row'):
        a = row.attrib
        folder_id = int(a['folderID'])
        folder = {
            'id': folder_id,
            'name': a['folderName'], # "" = toplevel
            'bookmarks': {},
        }
        bookmarks = row.find('rowset')
        for row in bookmarks.findall('row'):
            a = row.attrib
            bookmark_id = int(a['bookmarkID'])
            folder['bookmarks'][bookmark_id] = {
                'id': bookmark_id,
                'name': a['memo'],
                'creator_id': int(a['creatorID']),
                'created_ts': api.parse_ts(a['created']),
                'item_id': int(a['itemID']),
                'type_id': int(a['typeID']),
                'location_id': int(a['locationID']),
                'x': float(a['x']),
                'y': float(a['y']),
                'z': float(a['z']),
                'note': a['note'],
            }
        result[folder_id] = folder
    return result

# vim: set ts=4 sts=4 sw=4 et:
