import gspread
from datetime import datetime


class GSheets:

    column_map = {
        "date": "date",
        "time": "time",
        "timestamp": "entered_timestamp",
        "amount": "amount",
        "category": "category",
        "sub category": "sub_category",
        "payment mode": "paid_using",
        "paid to": "paid_to",
        "locality": "locality",
        "city": "city",
        "state": "state",
        "country": "country",
        "latitude": "latitude",
        "longitude": "longitude"
    }

    def __init__(self, config_path):
        self.sevice_acc = gspread.service_account(filename=config_path)

    def set_workbook(self, workbook_name):
        self.workbook = self.sevice_acc.open(workbook_name)

    def set_column_map(self, column_map):
        self.column_map = column_map

    def update_cmap_field(self, field_name, value):
        self.column_map[field_name] = value

    def get_transformed_record(self, record):
        transformed_record = {v: f'{record[k]}'.lower().strip() for k, v in self.column_map.items()}
        transformed_record["amount"] = float(transformed_record["amount"])
        transformed_record["date"] = str(datetime.strptime(transformed_record["date"], "%m/%d/%Y").date())
        transformed_record["sub_category"] = transformed_record["sub_category"].replace(' ', '').split(',')
        transformed_record["sub_category"] = None if transformed_record["sub_category"][0] == '' else transformed_record["sub_category"]
        return transformed_record

    def get_sheet_data(self, sheet_name):
        sheet = self.workbook.worksheet(sheet_name)
        data = sheet.get_all_records()
        transformed_data = [self.get_transformed_record(record) for record in data]

        return transformed_data
