from DB.docs_fetching import client

spreadsheet = client.open_by_key("1inwAYzAOwApeIDUEMoQft9eodHDMBscRt7orUwHov2g")

worksheet = spreadsheet.sheet1
all_values = worksheet.get_all_values()

installers = sorted(all_values[1:])