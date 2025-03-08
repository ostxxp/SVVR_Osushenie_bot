import gspread
from google.oauth2.service_account import Credentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

credentials = Credentials.from_service_account_file('../credentials.json', scopes=scope)
client = gspread.authorize(credentials)

# spreadsheet = client.create("My New Spreadsheet3")
# spreadsheet.share('svvr.osushenie@gmail.com', perm_type='user', role='owner')
# print(spreadsheet.url)

