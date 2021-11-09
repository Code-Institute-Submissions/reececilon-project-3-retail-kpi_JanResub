import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Retailing')

def retail_independents(ldata, data):
    independents = ldata

    data_type = input(f'Input {data}:\n')
    independents.append(data_type)
    return independents

def convert_to_int(data):
    int_list = []
    for ind in data:
        int_list.append(int(ind))
    return int_list

def add_to_worksheet(data, sheet):
    print(data)
    print(f'Updating {sheet}...')
    add_worksheet = SHEET.worksheet(sheet)
    add_worksheet.append_row(data)
    print(f'{sheet} update complete.')

def main():
    independs = [] 
    footfall = retail_independents(independs, "footfall")
    total_sales = retail_independents(footfall, "total sales")
    num_sales = retail_independents(total_sales, "num sales")
    independents = retail_independents(num_sales, "num items sold")
    int_data = convert_to_int(independents)
    add_to_worksheet(int_data, 'independents')

main()