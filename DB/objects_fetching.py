from docs_fetching import client

spreadsheet = client.open_by_key('1b2IQ7uB_bh2h0kkpfYfU7AWbOBo8cc6umBHwQW7462M')
worksheet = spreadsheet.sheet1
all_values = worksheet.get_all_values()

headers = all_values[3]
data_temp = all_values[4:]

data = []

for d in data_temp:
    data.append(list(filter(lambda x: any(x), d))[:3])

def fetch_objects(id):
    name =
    for d in data:
        try:
            if d[2] = :
                print(d[1])
        except:
            pass

