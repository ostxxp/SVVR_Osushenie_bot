from DB.docs_fetching import client

spreadsheet = client.open_by_key("104Br__eJuDxp1Vm4AS3xCmjVAsTqc5y0jZZgiQ9ljx8")

worksheet = spreadsheet.sheet1
all_values = worksheet.get_all_values()

installers = sorted(all_values[1:])