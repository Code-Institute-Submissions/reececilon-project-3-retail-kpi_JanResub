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


def begin():
    """
    Starts the application, allowing the user to chose what they would like to do would like to do
    """

    print("""
    ----------------------MENU-----------------------
    1. Input today's sales figures and calculate KPIs\n\
    2. View today's sales target\n\
    3. Exit\n
    """)

    while True:
        user_choice = int(input("\nWhich task would you like to complete: \n"))
        if user_choice == 1:
            print("\nOkay, ready to input today's sales figures...\n")
            main()
        elif user_choice == 2:
            sales_target = SHEET.worksheet('sum sales target').col_values(1)[-1]
            
            print("Here is today's sales target in £: ")
            print(sales_target)
        elif user_choice == 3:
            print("You chose to exit this app...")
            exit_program()
            break
        else:
            print("Invalid choice. Please choose from the menu above a number from 1 to 3.\n")
    
def exit_program():
    """
    Exits the application.
    """

    print("------------------------------------------------------")
    print("----------------------Thank you!----------------------")
    print("-----------------------GOODBYE------------------------")


def list_retail_independents(ldata, data):
    """
    Lists the inputs required for the worksheet
    """

    independents = ldata

    if len(independents) == 0:
        print("Footfall is the number of clients or customers that enter the store.")
    elif len(independents) == 1:
        print("\nsum sales is the total income made during business hours.")
    elif len(independents) == 2:
        print("\nnum sales is the number of customers that made a purchase.")
    else:
        print("\nnum items is the total number of items sold.")

    data_type = input(f'Submit {data}:\n')
    independents.append(data_type)
    return independents


def convert_to_int(data):
    """
    Converts the sales_figures list items into integers and checks that data is valid by throwing an error when data is invalid
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

    print(f'\nUpdating {sheet}...\n')
    add_worksheet = SHEET.worksheet(sheet)
    add_worksheet.append_row(data)
    print(f'{sheet} worksheet updated.\n')


def conversion():
    """
    Conversion is the number of customers that enter the store and make a purchase
    """

    dependents1 = []
    f_fall_recent = SHEET.worksheet('sales figures').col_values(1)[-1]
    num_sales_recent = SHEET.worksheet('sales figures').col_values(3)[-1]

    conversion = int(num_sales_recent) / int(f_fall_recent) * 100

    dependents1.append(conversion)
    return dependents1


def items_per_customer(data):
    """
    Calculates the items per customer: IPC. and appends to the dependents list
    """

    dependents1 = data
    total_items_sold_recent = SHEET.worksheet('sales figures').col_values(4)[-1]
    num_sales_recent = SHEET.worksheet('sales figures').col_values(3)[-1]

    ipc = int(total_items_sold_recent) / int(num_sales_recent)

    dependents1.append(ipc)
    return dependents1


def average_sale_per_customer(data):
    """
    Calculates the average sale per customer: APC. and then appends this to the dependents list.
    """

    dependents1 = data
    sum_sales_recent = SHEET.worksheet('sales figures').col_values(2)[-1]
    num_sales_recent = SHEET.worksheet('sales figures').col_values(3)[-1]

    apc = int(sum_sales_recent) / int(num_sales_recent)

    dependents1.append(apc)
    return dependents1


def sales_expectation(data):
    """
    compares the sum sales to the target sum sales to quantify how they vary
    """
    dependents1 = data
    sum_sales_recent = SHEET.worksheet('sales figures').col_values(2)[-1]
    target_sum_sales = SHEET.worksheet('sum sales target').col_values(1)[-1]

    exp = ((int(sum_sales_recent) - int(target_sum_sales)) / int(target_sum_sales)) * 100

    dependents1.append(exp)
    return dependents1


def next_sum_sales_target():
    """
    calculates the next days target sales by taking an average of the 5 sum sales
    """

    dependents2 = []
    sum_sales = SHEET.worksheet('sales figures').col_values(2)
    total = 0

    for i in range(len(sum_sales)):
        if (len(sum_sales) - i) <= 5:
            total += int(sum_sales[i])
    
    next_sales_target = total / 5
    
    dependents2.append(next_sales_target)

    return dependents2


def view_worksheet(data):
    """
    Allows the user to view most recently updated worksheet data
    """

    

    list1 = []
    list2 = []
    val = SHEET.worksheet(data)

    
    for ind in range(1, 5):
        value1 = val.col_values(ind)[0]
        value2 = val.col_values(ind)[-1]
        list1.append(value1)
        list2.append(value2)
    
    request = zip(list1,list2)

    print(dict(request))


def reset():
    SHEET.worksheet.delete_row(8)


def options():
    """
    Gives the user further options to choose from
    """

    print("""
    ----------------------MENU-----------------------
    1. View updated sales figures\n\
    2. View updated KPIs\n\
    3. View next day sales target\n\
    4. Reset most recent sales figures and KPIs\n\
    5. Exit\n
    """)

    while True:
        user_choice = int(input("\nWhich task would you like to complete: \n"))
        if user_choice == 1:
            print("\nOkay, here are the sales figures you submitted today...\n")
            view_worksheet("sales figures")
        elif user_choice == 2:
            print("\nOkay, here are the updated KPIs from today...\n")
            view_worksheet("KPIs")
        elif user_choice == 3:
            print("\nOkay, here is the sales target for tomorrow...\n")
            sales_target = SHEET.worksheet("sum sales target").col_values(1)[-1]
            print(f'Next Trg: {sales_target}')
        elif user_choice == 4:
            print("\nRight, I will reset the last sales figures and KPIs...\n")
            reset()
        elif user_choice == 5:
            print("\nYou chose to exit this app...")
            exit_program()
            break
        else:
            print("Invalid choice. Please choose from the menu above a number from 1 to 5.\n")


def main():
    independs = [] 
    footfall = list_retail_independents(independs, "footfall")
    total_sales = list_retail_independents(footfall, "sum sales")
    num_sales = list_retail_independents(total_sales, "num sales")
    sales_figures = list_retail_independents(num_sales, "num items sold")
    ind_data = convert_to_int(sales_figures)
    add_to_worksheet(ind_data, 'sales figures')
    convert = conversion()
    ipc = items_per_customer(convert)
    apc = average_sale_per_customer(ipc)
    dep1 = sales_expectation(apc)
    add_to_worksheet(dep1, 'KPIs')
    next_sum = next_sum_sales_target()
    add_to_worksheet(next_sum, 'sum sales target')
    options()


print("------------------------------------------------------")
print("-----------------------Welcome!-----------------------")
print("-----------------This is a retail app-----------------")
print("-------This app allows the user to analyse KPIs-------")
print("---------------Choose from the menu below-------------")

begin()
