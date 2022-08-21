# pass: Bsfl17tUa00KwlG5
from pymongo import MongoClient
from gsheet import GSheets
import json

with open('./config/mongo_creds.json') as f:
    creds = json.load(f)

client = MongoClient(f"mongodb+srv://{creds['username']}:{creds['password']}@{creds['database_name']}.4jhpj1c.mongodb.net/?retryWrites=true&w=majority")

db = client.expense_tracker

expenses = db.expenses

gsheets = GSheets("./config/expense-tracker-358105-47cb813a72fa.json")
gsheets.set_workbook('expense_tracker')

column_map = {
    "Date": "date",
    "Time": "time",
    "Timestamp": "entered_timestamp",
    "Amount": "amount",
    "Category": "category",
    "Sub Category (Separate if Multiple by ,)": "sub_category",
    "Paid Using": "paid_using",
    "Paid To": "paid_to",
    "Locality": "locality",
    "City": "city",
    "State": "state",
    "Country": "country",
    "Latitude": "latitude",
    "Longitude": "longitude"
}

old_payments_data = gsheets.get_sheet_data('payments')

gsheets.set_column_map(column_map)
form_responses_data = gsheets.get_sheet_data('form_responses')

expenses.insert_many(old_payments_data + form_responses_data)