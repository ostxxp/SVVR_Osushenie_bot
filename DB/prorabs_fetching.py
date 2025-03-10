from DB.docs_fetching import client

spreadsheet = client.open_by_key('18aKX9sXEbmT1Hd_bK6RL_5gJ8cteRlv5d-vclL1SqHw')
worksheet = spreadsheet.sheet1
all_values = worksheet.get_all_values()

headers = all_values[0]
prorabs = all_values[1:]

async def is_prorab(id):
    for prorab in prorabs:
        if int(prorab[0]) == id:
            return True
    return False