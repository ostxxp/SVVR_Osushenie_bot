from DB.docs_fetching import client
from DB.prorabs_fetching import prorabs

spreadsheet = client.open_by_key('1z6pOvc5rZc0bjE-Zy5GsyX0t4Q-ndvktVEV0eL1CI8o')
worksheet = spreadsheet.sheet1
all_values = worksheet.get_all_values()


headers = all_values[3]
data_temp = all_values[4:]

data = []

for d in data_temp:
    data.append(list(filter(lambda x: any(x), d))[:3])


def fetch_objects(id):
    for prorab in prorabs:
        if int(prorab[0]) == id:
            name = prorab[1]
            break
    else:
        return None
    objects = []
    for d in data:
        try:
            if d[2] == name:
                objects.append(d[1])
        except:
            pass
    return objects


