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
SALES_FIGURE_SHEET = SHEET.worksheet('sales figures')
KPI_SHEET = SHEET.worksheet('KPIs')
SS_TARGET_SHEET = SHEET.worksheet('sum sales target')


def begin():
    """
    Starts the application,
    allowing the user to choose
    what they would like to do.
    """

    while True:
        print("""
        ----------------------MENU-----------------------
        1. Input today's sales figures and calculate KPIs\n\
        2. View today's sales target\n\
        3. Exit\n
        """)

        user_choice = input("\nWhich task would you like to complete: \n")
        if user_choice == '1':
            print("\nOkay, ready to input today's sales figures...\n")
            main()
            break
        elif user_choice == '2':
            sales_sheet = SS_TARGET_SHEET.col_values(1)[-1]
            print("Here is today's sales target in £: ")
            print(sales_sheet)
        elif user_choice == '3':
            print("You chose to exit this app...")
            exit_program()
            break
        else:
            print("Invalid choice. Please choose a number 1- 3.\n")
        


def exit_program():
    """
    Exits the application.
    """

    print("------------------------------------------------------")
    print("----------------------Thank you!----------------------")
    print("--------------------SHUTTING DOWN...------------------")
    print("-----------------------GOODBYE------------------------")


def list_sales_figures(ldata, data):
    """
    Lists the inputs required for
    the worksheet and validates the input data
    to prevent negative and non-integer
    values from being passed
    """

    independents = ldata

    if len(independents) == 0:
        print("Footfall is the number of customers that enter the store.")
    elif len(independents) == 1:
        print("\nsum sales is the revenue made during business hours.")
        print("Measured in £")
    elif len(independents) == 2:
        print("\nnum sales is the number of customers that made a purchase.")
    else:
        print("\nnum items is the total number of items sold.")

    data_type = "strings"
    while data_type.isdigit() == False:
        data_type = input(f'Submit {data}:\n')

        if data_type.isdigit() == False:
            print(f'{data_type} is not an integer.')
            print(f'{data} must be an integer number. Please try again.')

    print(data_type)
    independents.append(data_type)

    return independents


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
    Conversion is the number of customers
    that enter the store and make a purchase
    as a percentage.
    """

    dependents1 = []
    f_fall_recent = SALES_FIGURE_SHEET.col_values(1)[-1]
    num_sales_recent = SALES_FIGURE_SHEET.col_values(3)[-1]

    conversion = int(num_sales_recent) / int(f_fall_recent) * 100
    dependents1.append(conversion)

    return dependents1


def items_per_customer(data):
    """
    Calculates the items per customer: IPC
    and appends to the KPIs list.
    """

    dependents1 = data
    total_items_sold_recent = SALES_FIGURE_SHEET.col_values(4)[-1]
    num_sales_recent = SALES_FIGURE_SHEET.col_values(3)[-1]

    ipc = int(total_items_sold_recent) / int(num_sales_recent)
    dependents1.append(ipc)

    return dependents1


def average_sale_per_customer(data):
    """
    Calculates the average sale per customer: APC
    and then appends this to the dependents list.
    """

    dependents1 = data
    sum_sales_recent = SALES_FIGURE_SHEET.col_values(2)[-1]
    num_sales_recent = SALES_FIGURE_SHEET.col_values(3)[-1]

    apc = int(sum_sales_recent) / int(num_sales_recent)
    dependents1.append(apc)

    return dependents1


def sales_expectation(data):
    """
    compares the sum sales to the target sum sales
    to quantify how they vary as a percentage.
    """

    dependents1 = data
    sum_sales_recent = SALES_FIGURE_SHEET.col_values(2)[-1]
    target_sum_sales = SS_TARGET_SHEET.col_values(1)[-1]

    dif = (int(sum_sales_recent) - float(target_sum_sales))
    exp = (dif / float(target_sum_sales)) * 100
    dependents1.append(exp)

    return dependents1


def next_sum_sales_target():
    """
    calculates the next days target sales
    by taking an average of the 5 sum sales.
    """

    dependents2 = []
    sum_sales = SALES_FIGURE_SHEET.col_values(2)
    total = 0

    for i in range(len(sum_sales)):
        if (len(sum_sales) - i) <= 5:
            total += int(sum_sales[i])

    next_sales_target = total / 5
    dependents2.append(next_sales_target)

    return dependents2


def view_worksheet(data):
    """
    Allows the user to view most
    recently updated worksheet data
    """

    list1 = []
    list2 = []
    val = SHEET.worksheet(data)

    for ind in range(1, 5):
        value1 = val.col_values(ind)[0]
        value2 = val.col_values(ind)[-1]
        list1.append(value1)
        list2.append(value2)
    request = zip(list1, list2)

    print(dict(request))


def reset():
    """
    Resets the Input sales figures,
    calculated KPIs and the next day sales target.
    """

    collumn1 = SALES_FIGURE_SHEET.col_values(1)
    last_row1 = len(collumn1)

    print("Today's sales figures have been reset.")
    wsheet_sales = SALES_FIGURE_SHEET.delete_rows(last_row1)

    collumn2 = KPI_SHEET.col_values(1)
    last_row2 = len(collumn2)

    print("KPIs for today have been reset.")
    wsheet_kpi = KPI_SHEET.delete_rows(last_row2)

    collumn3 = SS_TARGET_SHEET.col_values(1)
    last_row3 = len(collumn3)

    print("Recent sum sales target has been reset.")
    wsheet_target = SS_TARGET_SHEET.delete_rows(last_row3)

    begin()


def options():
    """
    Gives the user further options to choose from
    """

    print("Sales figures, KPIs and sales target have been updated.")
    print("Select from the menu below, What you would like to do next.")

    while True:
        print("""
        ----------------------MENU-----------------------
        1. View updated sales figures\n\
        2. View updated KPIs\n\
        3. View next day sales target\n\
        4. Reset most recent sales figures and KPIs\n\
        5. Exit\n
        """)
        user_choice = input("\nWhich task would you like to complete: \n")
        if user_choice == '1':
            print("\nOkay, here are the sales figures for today...\n")
            view_worksheet("sales figures")
        elif user_choice == '2':
            print("\nOkay, here are the updated KPIs from today...\n")
            view_worksheet("KPIs")
        elif user_choice == '3':
            print("\nOkay, here is the sales target for tomorrow,")
            print("measured in £:\n")
            sales_target = SS_TARGET_SHEET.col_values(1)[-1]
            print(f'Next Trg: {sales_target}')
        elif user_choice == '4':
            print("\nRight, I will reset the last sales figures and KPIs...\n")
            reset()
            break
        elif user_choice == '5':
            print("\nYou chose to exit this app...")
            exit_program()
            break
        else:
            print("Invalid choice. Please choose a number from 1 to 5.\n")


def main():
    """
    The main function that calls functions for core purpose of app
    """

    independs = []
    footfall = list_sales_figures(independs, "footfall")
    total_sales = list_sales_figures(footfall, "sum sales")
    num_sales = list_sales_figures(total_sales, "num sales")
    sales_data = list_sales_figures(num_sales, "num items sold")
    add_to_worksheet(sales_data, 'sales figures')
    con = conversion()
    ipc = items_per_customer(con)
    apc = average_sale_per_customer(ipc)
    exp = sales_expectation(apc)
    add_to_worksheet(exp, 'KPIs')
    next_sum = next_sum_sales_target()
    add_to_worksheet(next_sum, 'sum sales target')
    options()


print("------------------------------------------------------")
print("-----------------------Welcome!-----------------------")
print("-----------------This is a retail app-----------------")
print("-------This app allows the user to analyse KPIs-------")
print("---------------Choose from the menu below-------------")


begin()
