from DB.docs_fetching import client

spreadsheet = client.open_by_key("1mAPOj4jqSYw8E7ZolNr-gVbdjHoVYERdW_zBbhNzoLQ")

worksheet = spreadsheet.sheet1
all_values = worksheet.get_all_values()

groups = []
for v in all_values[6:]:
    if v[0] != '':
        groups.append(v[0:3])

def sort_key(item):
    return tuple(map(int, item[0].split('.')))

sorted_groups = sorted(groups, key=sort_key)

async def get_group_name(id):
    name = ""
    for group in sorted_groups:
        if group[0] == id:
            name += group[1].strip()
            break
    if id.count('.') == 2:
        target = '.'.join(id.split('.')[:-1])
        for group in sorted_groups:
            if group[0] == target:
                name = group[1] + " *(" + name + ")*"
    return name

async def get_work_type(id):
    for group in sorted_groups:
        if group[0] == id:
            return group[2]

