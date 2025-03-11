import gspread
from google.oauth2.service_account import Credentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

credentials = Credentials.from_service_account_file('../credentials.json', scopes=scope)
client = gspread.authorize(credentials)
