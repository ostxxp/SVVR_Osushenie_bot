from DB.docs_fetching import client

spreadsheet = client.open_by_key('1b2IQ7uB_bh2h0kkpfYfU7AWbOBo8cc6umBHwQW7462M')
worksheet = spreadsheet.sheet1
all_values = worksheet.get_all_values()

spreadsheet = client.create("My New Spreadsheet3")
spreadsheet.share('svvr.osushenie@gmail.com', perm_type='user', role='writer')
worksheet.update_cell(1, 1, f'=HYPERLINK("{spreadsheet.url}"; "Ссылка")')

spreadsheets = client.list_spreadsheet_files()
for s in spreadsheets:
    print(s['name'])