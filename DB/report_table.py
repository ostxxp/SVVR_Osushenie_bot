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
    worksheet.update(f"{column}2", [[lines[0]]])
    print(lines)
    if len(lines) > 1:
        for k in range(1, len(lines) - 1):
            for i in range(len(all_values)):
                if str(lines[k].split()[0]) == (all_values[i][0]):
                    worksheet.update(f"{column}{i + 1}", [[float(lines[k].split()[1].strip())]])
                    break
        for i in range(len(all_values)):
            if all_values[i][5] == "Рабочие":
                k = i + 1
                for installer in sorted(lines[-1].split(',')):
                    worksheet.update(f"{column}{k}", [[installer]])
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
    worksheet.update(f"{column}2", [[date[0].strip()]])

    for i in range(2, len(all_values)):
        if all_values[i][5] != "Рабочие" and all_values[i][0].count(".") > 0 and all_values[i][2] != '':
            worksheet.update(f"{column}{i + 1}", [['0']])



async def find_date(id, link, date):
    spreadsheet = client.open_by_key(link.split('/')[5])
    worksheet = spreadsheet.sheet1
    values = worksheet.row_values(2)

    for i in range(6, len(values)):
        if values[i] == date or values[i] == '':
            await database_funcs.set_column(id, chr(ord("A") + i + 1))
            return None

    await database_funcs.set_column(id, chr(ord("A") + len(values)))
    return None
