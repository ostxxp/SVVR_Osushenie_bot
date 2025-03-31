from DB.docs_fetching import client
from DB import database_funcs, objects_fetching


async def create_table_report(id):
    object = await objects_fetching.fetch_objects_by_name(await database_funcs.get_obj_name(id))
    link = object[3]

    with open(f'report_info/{id}.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    spreadsheet = client.open_by_key(link.split('/')[5])
    worksheet = spreadsheet.sheet1
    all_values = worksheet.get_all_values()

    column = await database_funcs.get_column(id)
    worksheet.update_cell(2, int(column), lines[0])
    if len(lines) > 1:
        for k in range(1, len(lines) - 1):
            for i in range(len(all_values)):
                if str(lines[k].split()[0]) == (all_values[i][0]):
                    worksheet.update_cell(i + 1, int(column), float(lines[k].split()[1].strip()))
                    break
        for i in range(len(all_values)):
            if all_values[i][5] == "Рабочие":
                k = i + 1
                for installer in sorted(lines[-1].split(',')):
                    worksheet.update_cell(k, int(column), installer)
                    k += 1


async def fill_zeros(id):
    object = await objects_fetching.fetch_objects_by_name(await database_funcs.get_obj_name(id))
    link = object[3]

    spreadsheet = client.open_by_key(link.split('/')[5])
    worksheet = spreadsheet.sheet1
    all_values = worksheet.get_all_values()

    column = await database_funcs.get_column(id)

    with open(f'report_info/{id}.txt', 'r', encoding='utf-8') as file:
        date = file.readlines()
    worksheet.update_cell(2, int(column), date[0].strip())


async def find_date(id, link, date):
    spreadsheet = client.open_by_key(link.split('/')[5])
    worksheet = spreadsheet.sheet1
    values = worksheet.row_values(2)
    for dates in values:
        if date == dates.strip():
            return "exists"
    await database_funcs.set_column(id, str(len(values) + 1))
    return None
