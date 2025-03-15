from DB.docs_fetching import client

spreadsheet = client.open_by_key("1EPmDWO9po2BOW6ohurI13ojTYocmfKqVmyQotjbyyI0")

worksheet = spreadsheet.sheet1
all_values = worksheet.get_all_values()

installers = sorted(all_values[1:])