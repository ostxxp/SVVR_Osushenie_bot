from DB.docs_fetching import client

spreadsheet = client.open_by_key("1kQTIfKirLZ55PV7tuKxMtjw6106AiuNkJ3mYp-m3LL0")

worksheet = spreadsheet.sheet1
all_values = worksheet.get_all_values()

for v in all_values[6:]:
    print(v)