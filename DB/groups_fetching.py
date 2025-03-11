from DB.docs_fetching import client

spreadsheet = client.open_by_key("1aHP1n2x4Kqytd2YSYTPk6Yhvnh7LQ7QAwB5AFQe0ssw")

worksheet = spreadsheet.sheet1
all_values = worksheet.get_all_values()

groups = []
for v in all_values[6:]:
    if v[0] != '':
        groups.append(v)

def sort_key(item):
    return tuple(map(int, item[0].split('.')))

sorted_groups = sorted(groups, key=sort_key)

s = "1.2.3"
print('.'.join(s.split('.')[:-1]))

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

