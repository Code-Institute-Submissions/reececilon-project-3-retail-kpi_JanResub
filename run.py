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

def list_retail_independents(ldata, data):
    """
    Lists the inputs required for the worksheet
    """

    independents = ldata

    data_type = input(f'Input {data}:\n')
    independents.append(data_type)
    return independents

def convert_to_int(data):
    """
    Converts the inouts into integers and checks that data is valid by throwing an error when data 
    """
    try:
        int_list = []
        for ind in data:
            int_list.append(int(ind))
    except:
        print("Invalid input! Input values must be integer values. Please try again.")
        main()

    return int_list

def add_to_worksheet(data, sheet):
    """
    Updates the worksheet with the inputs
    """

    print(data)
    print(f'Updating {sheet}...')
    add_worksheet = SHEET.worksheet(sheet)
    add_worksheet.append_row(data)
    print(f'{sheet} update complete.')

def conversion():
    """
    Conversion is the number of customers that enter the store and make a purchase
    """

    dependents1 = []
    f_fall_recent = SHEET.worksheet('independents').col_values(1)[-1]
    num_sales_recent = SHEET.worksheet('independents').col_values(3)[-1]

    conversion = int(num_sales_recent) / int(f_fall_recent) * 100

    dependents1.append(conversion)
    return dependents1

def items_per_customer(data):
    """
    Calculates the items per customer: IPC. and appends to the dependents list
    """

    dependents1 = data
    total_items_sold_recent = SHEET.worksheet('independents').col_values(4)[-1]
    num_sales_recent = SHEET.worksheet('independents').col_values(3)[-1]

    ipc = int(total_items_sold_recent) / int(num_sales_recent)

    dependents1.append(ipc)
    return dependents1

def average_sale_per_customer(data):
    """
    Calculates the average sale per customer: APC. and then appends this to the dependents list.
    """

    dependents1 = data
    sum_sales_recent = SHEET.worksheet('independents').col_values(2)[-1]
    num_sales_recent = SHEET.worksheet('independents').col_values(3)[-1]

    apc = int(sum_sales_recent) / int(num_sales_recent)

    dependents1.append(apc)
    return dependents1

def sales_expectation(data):
    """
    compares the sum sales to the target sum sales to quantify how they vary
    """
    dependents1 = data
    sum_sales_recent = SHEET.worksheet('independents').col_values(2)[-1]
    target_sum_sales = SHEET.worksheet('dependents2').col_values(1)[-1]

    exp = ((int(sum_sales_recent) - int(target_sum_sales)) / int(target_sum_sales)) * 100

    dependents1.append(exp)
    return dependents1

def next_sum_sales_target():
    """
    calculates the next days target sales by taking an average of the 5 sum sales
    """

    dependents2 = []
    sum_sales = SHEET.worksheet('independents').col_values(2)
    total = 0

    for i in range(len(sum_sales)):
        if (len(sum_sales) - i) <= 5:
            total += int(sum_sales[i])
    
    next_sales_target = total / 5
    
    dependents2.append(next_sales_target)

    return dependents2
    
def main():
    independs = [] 
    footfall = list_retail_independents(independs, "footfall")
    total_sales = list_retail_independents(footfall, "total sales")
    num_sales = list_retail_independents(total_sales, "num sales")
    independents = list_retail_independents(num_sales, "num items sold")
    ind_data = convert_to_int(independents)
    add_to_worksheet(ind_data, 'independents')
    convert = conversion()
    ipc = items_per_customer(convert)
    apc = average_sale_per_customer(ipc)
    dep1 = sales_expectation(apc)
    add_to_worksheet(dep1, 'dependents1')
    next_sum = next_sum_sales_target()
    add_to_worksheet(next_sum, 'dependents2')

main()