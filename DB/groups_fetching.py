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
