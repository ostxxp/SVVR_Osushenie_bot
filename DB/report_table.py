from DB.docs_fetching import client
from DB.groups_fetching import sorted_groups

async def create_table_report(name):
    spreadsheet = client.create(name)
    worksheet = spreadsheet.sheet1
    worksheet.update("A1:F1", [["Наименование работ", "", "Ед. Изм.", "Общее кол-во", "Всего сделано", "Осталось сделать"]])
    worksheet.update("B2", [["Дата"]])
    for i in range(len(sorted_groups)):
        worksheet.update(f"A{i+3}:C{i+3}", [sorted_groups[i]])

    spreadsheet.share(None, perm_type="anyone", role="reader")
    spreadsheet.share("osushenie.rf@gmail.com", perm_type="user", role="writer")
    spreadsheet.share("osusheniesvvr@gmail.com", perm_type="user", role="writer")

    return spreadsheet.url

async def find_row(link, number, date):
    spreadsheet = client.open_by_key(link.split('/')[5])
    worksheet = spreadsheet.sheet1
    all_values = worksheet.get_all_values()
    for i in range(len(all_values)):
        if all_values[i][0] == number:
            return f"{(await find_date(link, date))[0]}{i+1}"

async def fill_value(link, location, value):
    spreadsheet = client.open_by_key(link.split('/')[5])
    worksheet = spreadsheet.sheet1
    worksheet.update(location, [[value]])

async def find_date(link, date):
    spreadsheet = client.open_by_key(link.split('/')[5])
    worksheet = spreadsheet.sheet1
    values = worksheet.row_values(2)
    for i in range(6, len(values)):
        if values[i] == date or values[i] == '':
            return f"{chr(ord("A") + i + 1)}2"