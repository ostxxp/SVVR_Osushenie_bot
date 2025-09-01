from DB.docs_fetching import client

spreadsheet = client.open_by_key("1lpZoY8t4OZ7LrOl_5Bg_6zHziDsi84mvySVONN5le9E")

worksheet = spreadsheet.sheet1
all_values = worksheet.get_all_values()

groups = []
for i in range(3, len(all_values[0])):
    groups.append([all_values[0][i], all_values[1][i], all_values[2][i]])


async def get_group_name(id):
    name = ""
    for group in groups:
        if group[0] == id:
            name += group[1].strip()
            break
    if id.count('.') == 2:
        target = '.'.join(id.split('.')[:-1])
        for group in groups:
            if group[0] == target:
                name = group[1] + " *(" + name + ")*"
    return name

async def get_work_type(id):
    for group in groups:
        if group[0] == id:
            return group[2]

