from DB.docs_fetching import client

spreadsheet = client.open_by_key('1ueuVTglC9wVn4boUiz0S6FjNqWJbmlV43fhh4U4gJAE')
worksheet = spreadsheet.sheet1
all_values = worksheet.get_all_values()

headers = all_values[0]
prorabs = all_values[1:]

async def is_prorab(id):
    for prorab in prorabs:
        if prorab[0] != '' and int(prorab[0]) == id:
            return True
    return False

async def get_prorab_name(id):
    for prorab in prorabs:
        if prorab[0] != '' and int(prorab[0]) == id:
            return prorab[1]