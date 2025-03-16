import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

credentials = Credentials.from_service_account_file(str(Path('../credentials.json').absolute()), scopes=scope)
client = gspread.authorize(credentials)
