from DB.docs_fetching import client
from DB.prorabs_fetching import prorabs

spreadsheet = client.open_by_key('14_vnU5vfVVct8XNBgd8l9B-m05nuSV_nfT7zZpeYp94')
worksheet = spreadsheet.sheet1
all_values = worksheet.get_all_values()


headers = all_values[3]
data = all_values[4:]


async def fetch_objects_names(id):
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

async def fetch_objects_by_name(name):
    for d in data:
        if d[1] == name:
            return d


def add_link(location, link):
    worksheet.update(location, [[link]])


