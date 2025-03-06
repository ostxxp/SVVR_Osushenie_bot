from DB.docs_fetching import client

spreadsheet = client.open_by_key('1o2uMWFS7aAFK1lkWSGhuKTKmV6CY2Hn8JmKvxnFSXK4')
worksheet = spreadsheet.sheet1
all_values = worksheet.get_all_values()

headers = all_values[0]
prorabs = all_values[1:]
