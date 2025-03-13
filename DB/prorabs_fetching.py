from DB.docs_fetching import client

spreadsheet = client.open_by_key('13aR7j_s8xZNectiUu-mWDTDzs8iL31jliTTAfjTMgEg')
worksheet = spreadsheet.sheet1
all_values = worksheet.get_all_values()

headers = all_values[0]
prorabs = all_values[1:]

async def is_prorab(id):
    for prorab in prorabs:
        if int(prorab[0]) == id:
            return True
    return False

async def get_prorab_name(id):
    for prorab in prorabs:
        if int(prorab[0]) == id:
            return prorab[1]