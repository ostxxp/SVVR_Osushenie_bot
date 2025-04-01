from DB.docs_fetching import client

spreadsheet = client.open_by_key("1EPmDWO9po2BOW6ohurI13ojTYocmfKqVmyQotjbyyI0")

worksheet = spreadsheet.sheet1

async def fetch_installers():
    all_values = worksheet.get_all_values()
    return sorted(all_values[1:])