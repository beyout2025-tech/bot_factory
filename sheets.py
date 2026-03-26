import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("BotFactory").sheet1

def save_user(user_id, username):
    sheet.append_row([user_id, username])

def save_bot(user_id, bot_type, name):
    sheet.append_row([user_id, bot_type, name])
